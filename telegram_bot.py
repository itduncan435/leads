#!/usr/bin/env python3
"""
Telegram Bot for AIO Phone Intelligence Platform
Generation Modules Only - Options 1-6
Conversational bot with user input, file download, and clean output
"""

import os
import sys
import io
import json
import logging
import tempfile
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
)
from telegram.constants import ParseMode

# Import main module components
import main

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = "8856220575:AAEjX6A4OkYz6QGVJVsib2PuVClHF_2GGVY"

# Conversation states
(
    SELECTING_MODULE,
    ASKING_COUNT,
    ASKING_BANK,
    ASKING_BRANCH,
    PROCESSING,
    DOWNLOADING,
) = range(6)

# Store user sessions
user_sessions: Dict[int, Dict[str, Any]] = {}


class BotUI(main.FuturisticUI):
    """Custom UI for Telegram bot that stores output for sending."""

    def __init__(self):
        super().__init__()
        self.telegram_messages: list[str] = []

    def get_prompt(self, message: str, default: str = "") -> str:
        """Return default value directly without prompting."""
        return default

    def _get_phone_input(self) -> Optional[str]:
        """Return a generated phone number instead of prompting."""
        return main.generate_phone_number("1")

    def console_print(self, text: str):
        """Capture console output for Telegram."""
        self.telegram_messages.append(text)


class BotHandlers(main.MenuHandlers):
    """Handlers that use BotUI and avoid stdin."""

    def __init__(self, ui: BotUI):
        super().__init__(ui)
        self.selected_bank = None
        self.selected_state = None
        self.branch_mode = "RANDOM"
        self.last_results_file = None
        self.user_count = None
        self.user_area_code = ""
        self.user_branch_mode = "RANDOM"
        self.user_selected_state = None
        self.user_country = "US"
        self.user_institution = None

    def get_prompt(self, message: str, default: str = "") -> str:
        """Return default value directly without prompting."""
        msg_lower = message.lower()
        if "bank number" in msg_lower or "select bank" in msg_lower:
            if self.selected_bank:
                for idx, bank in enumerate(main.US_BANKS, 1):
                    if bank["name"] == self.selected_bank["name"]:
                        return str(idx)
            return "1"
        if "branch mode" in msg_lower or "state code" in msg_lower:
            if self.user_selected_state:
                return self.user_selected_state
            return self.user_branch_mode or default
        if "how many" in msg_lower or ("numbers" in msg_lower and "generate" in msg_lower) or "count" in msg_lower or "records" in msg_lower:
            if self.user_count is not None:
                return str(self.user_count)
            return default
        if "area code" in msg_lower:
            return self.user_area_code or default
        if "country" in msg_lower:
            return self.user_country or default
        if "institution" in msg_lower:
            if self.user_institution is not None:
                return str(self.user_institution + 1)
            return "1"
        return default

    def _get_phone_input(self) -> Optional[str]:
        """Return a generated phone number instead of prompting."""
        return main.generate_phone_number("1")


def get_user_session(user_id: int) -> Dict[str, Any]:
    """Get or create user session."""
    if user_id not in user_sessions:
        ui = BotUI()
        user_sessions[user_id] = {
            "ui": ui,
            "handlers": BotHandlers(ui),
            "state": SELECTING_MODULE,
            "data": {},
            "module": None,
        }
    return user_sessions[user_id]


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Get main menu keyboard with Generation Modules only."""
    keyboard = [
        [
            InlineKeyboardButton("🏦 American First Credit Union", callback_data="module_1"),
            InlineKeyboardButton("📞 Phone Number Grabber", callback_data="module_2"),
        ],
        [
            InlineKeyboardButton("🏛️ USA Banks Database", callback_data="module_3"),
            InlineKeyboardButton("🍁 Canada Banks Database", callback_data="module_4"),
        ],
        [
            InlineKeyboardButton("₿ Crypto Wallet Scanner", callback_data="module_5"),
            InlineKeyboardButton("📧 Amazon SES OTP", callback_data="module_6"),
        ],
        [
            InlineKeyboardButton("❌ Exit", callback_data="exit"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_bank_selection_keyboard() -> InlineKeyboardMarkup:
    """Get bank selection keyboard."""
    keyboard = []
    row = []
    for idx, bank in enumerate(main.US_BANKS, 1):
        row.append(InlineKeyboardButton(f"{idx}. {bank['name']}", callback_data=f"bank_{idx}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)


def get_branch_selection_keyboard(bank_name: str) -> InlineKeyboardMarkup:
    """Get branch selection keyboard."""
    if bank_name == "American First Credit Union":
        branch_states = sorted({b["state"] for b in main.AFCU_BRANCHES})
    elif bank_name in main.BANK_BRANCHES:
        branch_states = sorted({b["state"] for b in main.BANK_BRANCHES[bank_name]})
    else:
        branch_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                         "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                         "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                         "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                         "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    keyboard = []
    row = []
    for state in branch_states:
        row.append(InlineKeyboardButton(state, callback_data=f"state_{state}"))
        if len(row) == 4:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("🎲 Random Branch", callback_data="state_RANDOM")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_bank")])
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Get back button keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /start command."""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    session["state"] = SELECTING_MODULE
    session["data"] = {}
    session["module"] = None

    welcome_text = """╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗
║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝
╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═
   HACKER TERMINAL v3.3.3

📱 TELEGRAM BOT INTERFACE
📞 DATABASE MODULES ONLY

Select a module to begin:"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )
    return SELECTING_MODULE


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button callbacks."""
    query: CallbackQuery = update.callback_query
    user_id = update.effective_user.id
    session = get_user_session(user_id)

    await query.answer()

    if query.data == "exit":
        await query.edit_message_text(
            "✅ [SUCCESS] EXITING HACKER TERMINAL...\n\nThank you for using the Telegram Bot Interface.",
            reply_markup=None
        )
        return ConversationHandler.END

    if query.data == "back_main":
        session["state"] = SELECTING_MODULE
        session["data"] = {}
        session["module"] = None
        await query.edit_message_text(
            "╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗\n"
            "║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝\n"
            "╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═\n"
            "   HACKER TERMINAL v3.3.3\n\n"
            "📱 TELEGRAM BOT INTERFACE\n"
            "📞 DATABASE MODULES ONLY\n\n"
            "Select a module to begin:",
            reply_markup=get_main_keyboard()
        )
        return SELECTING_MODULE

    if query.data.startswith("module_"):
        module_num = int(query.data.split("_")[1])
        if 1 <= module_num <= 6:
            session["module"] = module_num
            session["state"] = ASKING_COUNT
            session["data"] = {}

            module_names = {
                1: "🏦 American First Credit Union",
                2: "📞 Phone Number Grabber",
                3: "🏛️ USA Banks Database",
                4: "🍁 Canada Banks Database",
                5: "₿ Crypto Wallet Scanner",
                6: "📧 Amazon SES OTP",
            }

            await query.edit_message_text(
                f"✅ Selected: {module_names[module_num]}\n\n"
                f"How many records would you like to generate?\n"
                f"Default: 10\n\n"
                f"Please enter a number (1-500):",
                reply_markup=get_back_keyboard()
            )
            return ASKING_COUNT
        else:
            await query.edit_message_text(
                "❌ [ERROR] Invalid option selected.\n\nPlease use /start to return to main menu.",
                reply_markup=get_main_keyboard()
            )
            return SELECTING_MODULE

    if query.data.startswith("bank_"):
        bank_idx = int(query.data.split("_")[1]) - 1
        if 0 <= bank_idx < len(main.US_BANKS):
            session["data"]["bank_idx"] = bank_idx
            session["state"] = ASKING_BRANCH
            bank = main.US_BANKS[bank_idx]
            await query.edit_message_text(
                f"✅ Selected Bank: {bank['name']}\n"
                f"Routing: {bank['routing']}\n"
                f"SWIFT: {bank['swift']}\n\n"
                f"Select branch state or Random:",
                reply_markup=get_branch_selection_keyboard(bank["name"])
            )
            return ASKING_BRANCH
        else:
            await query.edit_message_text(
                "❌ [ERROR] Invalid bank selected.\n\nPlease use /start to return to main menu.",
                reply_markup=get_main_keyboard()
            )
            return SELECTING_MODULE

    if query.data.startswith("state_"):
        branch_mode = query.data.split("_")[1]
        session["data"]["branch_mode"] = branch_mode
        session["state"] = PROCESSING

        bank_idx = session["data"].get("bank_idx", 0)
        bank = main.US_BANKS[bank_idx]
        count = session["data"].get("count", 10)

        await query.edit_message_text(
            f"✅ Bank: {bank['name']}\n"
            f"✅ Branch: {branch_mode}\n\n"
            f"🔄 Generating {count} records...\n"
            f"Please wait...",
            reply_markup=get_back_keyboard()
        )
        return PROCESSING

    if query.data == "back_bank":
        session["state"] = ASKING_BANK
        await query.edit_message_text(
            "Select a bank:",
            reply_markup=get_bank_selection_keyboard()
        )
        return ASKING_BANK

    return SELECTING_MODULE


async def handle_count_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle user count input."""
    user_id = update.effective_user.id
    session = get_user_session(user_id)

    try:
        count = int(update.message.text.strip())
        count = max(1, min(count, 500))
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid input. Please enter a number between 1-500.\n\n"
            "How many records would you like to generate?",
            reply_markup=get_back_keyboard()
        )
        return ASKING_COUNT

    session["data"]["count"] = count
    module_num = session.get("module", 1)
    ui = session["ui"]
    handlers = session["handlers"]
    handlers.user_count = count

    if module_num == 1:
        session["state"] = ASKING_BRANCH
        await update.message.reply_text(
            f"✅ Count set to: {count}\n\n"
            f"Select branch state or Random:",
            reply_markup=get_branch_selection_keyboard("American First Credit Union")
        )
        return ASKING_BRANCH
    elif module_num == 3:
        session["state"] = ASKING_BANK
        await update.message.reply_text(
            f"✅ Count set to: {count}\n\n"
            f"Select a bank:",
            reply_markup=get_bank_selection_keyboard()
        )
        return ASKING_BANK
    else:
        session["state"] = PROCESSING

    module_num = session.get("module", 1)
    module_names = {
        1: "American First Credit Union",
        2: "Phone Number Grabber",
        3: "USA Banks Database",
        4: "Canada Banks Database",
        5: "Crypto Wallet Scanner",
        6: "Amazon SES OTP",
    }

    processing_msg = await update.message.reply_text(
        f"🔄 [PROCESS] {module_names[module_num]}\n\n"
        f"Generating {count} records...\n"
        f"Please wait...",
        reply_markup=get_back_keyboard()
    )

    try:
        ui = session["ui"]
        handlers = session["handlers"]

        # Clear previous messages
        ui.telegram_messages = []

        # Map options to handlers
        handler_map = {
            1: handlers.handle_option_1,
            2: handlers.handle_option_2,
            3: handlers.handle_option_3,
            4: handlers.handle_option_4,
            5: handlers.handle_option_5,
            6: handlers.handle_option_6,
        }

        handler = handler_map.get(module_num)
        if handler:
            handler()

            # Use actual results file if available, otherwise fall back to console output
            if hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file):
                results_filepath = handlers.last_results_file
                results_filename = os.path.basename(results_filepath)
            else:
                # Fallback: create file from console output
                output_lines = ui.telegram_messages
                results_text = "\n".join(output_lines) if output_lines else f"{module_names[module_num]} - {count} records generated"
                timestamp = main.get_timestamp().replace(":", "-").replace(" ", "_")
                results_filename = f"{module_names[module_num].replace(' ', '_')}_{timestamp}.txt"
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                    f.write(results_text)
                    results_filepath = f.name

            # Send completion message
            await processing_msg.edit_text(
                f"✅ [COMPLETE] {module_names[module_num]}\n\n"
                f"Generated: {count} records\n"
                f"Status: Success\n\n"
                f"📥 Results preview and download below:",
                reply_markup=get_back_keyboard()
            )

            # Read actual results content
            try:
                with open(results_filepath, 'r', encoding='utf-8') as f:
                    results_content = f.read()
            except Exception as e:
                logger.warning(f"Could not read results file: {e}")
                results_content = None

            # Send results text if available
            if results_content:
                preview = results_content[:3000]
                if len(results_content) > 3000:
                    preview += "\n\n... (truncated, see full file below)"
                try:
                    await update.message.reply_text(
                        f"📋 Results:\n\n{preview}",
                        reply_markup=get_back_keyboard()
                    )
                except Exception as e:
                    logger.warning(f"Could not send preview: {e}")

            # Send file
            try:
                with open(results_filepath, 'rb') as f:
                    await update.message.reply_document(
                        document=InputFile(f, filename=results_filename),
                        caption=f"📄 {module_names[module_num]} - {count} records - Full results",
                        reply_markup=get_back_keyboard()
                    )
            except Exception as e:
                logger.error(f"Could not send file: {e}", exc_info=True)
                await update.message.reply_text(
                    f"❌ Could not send file. Results saved at:\n{results_filepath}",
                    reply_markup=get_back_keyboard()
                )

            # Clean up temp file if we created one
            if not hasattr(handlers, 'last_results_file') or not handlers.last_results_file or not os.path.exists(handlers.last_results_file):
                try:
                    os.unlink(results_filepath)
                except Exception:
                    pass

            session["state"] = SELECTING_MODULE
            return SELECTING_MODULE
        else:
            await processing_msg.edit_text(
                "❌ [ERROR] Handler not found.",
                reply_markup=get_back_keyboard()
            )
            return SELECTING_MODULE

    except Exception as e:
        logger.error(f"Error processing module {module_num}: {e}", exc_info=True)
        await processing_msg.edit_text(
            f"❌ [HACKER ERROR] {str(e)}\n\n"
            f"Use /start to return to main menu.",
            reply_markup=get_back_keyboard()
        )
        return SELECTING_MODULE


async def handle_bank_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle bank selection from callback."""
    query: CallbackQuery = update.callback_query
    user_id = update.effective_user.id
    session = get_user_session(user_id)

    await query.answer()

    if query.data == "back_main":
        session["state"] = SELECTING_MODULE
        session["data"] = {}
        session["module"] = None
        await query.edit_message_text(
            "╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗\n"
            "║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝\n"
            "╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═\n"
            "   HACKER TERMINAL v3.3.3\n\n"
            "📱 TELEGRAM BOT INTERFACE\n"
            "📞 DATABASE MODULES ONLY\n\n"
            "Select a module to begin:",
            reply_markup=get_main_keyboard()
        )
        return SELECTING_MODULE

    if query.data.startswith("bank_"):
        bank_idx = int(query.data.split("_")[1]) - 1
        if 0 <= bank_idx < len(main.US_BANKS):
            session["data"]["bank_idx"] = bank_idx
            bank = main.US_BANKS[bank_idx]
            module_num = session.get("module", 1)
            count = session["data"].get("count", 10)
            handlers.user_count = count

            if module_num == 3:
                session["state"] = PROCESSING
                handlers.selected_bank = bank

                # Clear previous messages
                ui.telegram_messages = []

                # Call handler
                handler_map = {
                    1: handlers.handle_option_1,
                    2: handlers.handle_option_2,
                    3: handlers.handle_option_3,
                    4: handlers.handle_option_4,
                    5: handlers.handle_option_5,
                    6: handlers.handle_option_6,
                }
                handler = handler_map.get(3)
                if handler:
                    try:
                        handler()

                        # Use actual results file if available
                        if hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file):
                            results_filepath = handlers.last_results_file
                            results_filename = os.path.basename(results_filepath)
                        else:
                            # Fallback: create file from console output
                            output_lines = ui.telegram_messages
                            results_text = "\n".join(output_lines) if output_lines else f"USA Banks Database - {count} records generated"
                            timestamp = main.get_timestamp().replace(":", "-").replace(" ", "_")
                            results_filename = f"USA_Banks_Database_{timestamp}.txt"
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                                f.write(results_text)
                                results_filepath = f.name

                        # Send completion message
                        await query.edit_message_text(
                            f"✅ [COMPLETE] USA Banks Database\n\n"
                            f"Bank: {bank['name']}\n"
                            f"Generated: {count} records\n"
                            f"Status: Success\n\n"
                            f"📥 Results preview and download below:",
                            reply_markup=get_back_keyboard()
                        )

                        # Read actual results content
                        try:
                            with open(results_filepath, 'r', encoding='utf-8') as f:
                                results_content = f.read()
                        except Exception as e:
                            logger.warning(f"Could not read results file: {e}")
                            results_content = None

                        # Send results text if available
                        if results_content:
                            preview = results_content[:3000]
                            if len(results_content) > 3000:
                                preview += "\n\n... (truncated, see full file below)"
                            try:
                                await query.message.reply_text(
                                    f"📋 Results:\n\n{preview}",
                                    reply_markup=get_back_keyboard()
                                )
                            except Exception as e:
                                logger.warning(f"Could not send preview: {e}")

                        # Send file
                        try:
                            with open(results_filepath, 'rb') as f:
                                await query.message.reply_document(
                                    document=InputFile(f, filename=results_filename),
                                    caption=f"📄 USA Banks Database - {bank['name']} - {count} records - Full results",
                                    reply_markup=get_back_keyboard()
                                )
                        except Exception as e:
                            logger.error(f"Could not send file: {e}", exc_info=True)
                            await query.message.reply_text(
                                f"❌ Could not send file. Results saved at:\n{results_filepath}",
                                reply_markup=get_back_keyboard()
                            )

                        # Clean up temp file if we created one
                        if not (hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file)):
                            try:
                                os.unlink(results_filepath)
                            except Exception:
                                pass

                        session["state"] = SELECTING_MODULE
                        return SELECTING_MODULE
                    except Exception as e:
                        logger.error(f"Error processing Module 3: {e}", exc_info=True)
                        await query.edit_message_text(
                            f"❌ [HACKER ERROR] {str(e)}\n\n"
                            f"Use /start to return to main menu.",
                            reply_markup=get_main_keyboard()
                        )
                        session["state"] = SELECTING_MODULE
                        return SELECTING_MODULE
                else:
                    await query.edit_message_text(
                        "❌ [ERROR] Handler not found.",
                        reply_markup=get_back_keyboard()
                    )
                    session["state"] = SELECTING_MODULE
                    return SELECTING_MODULE
            else:
                session["state"] = ASKING_BRANCH
                await query.edit_message_text(
                    f"✅ Selected Bank: {bank['name']}\n"
                    f"Routing: {bank['routing']}\n"
                    f"SWIFT: {bank['swift']}\n\n"
                    f"Select branch state or Random:",
                    reply_markup=get_branch_selection_keyboard(bank["name"])
                )
                return ASKING_BRANCH
        else:
            await query.edit_message_text(
                "❌ [ERROR] Invalid bank selected.\n\nPlease use /start to return to main menu.",
                reply_markup=get_main_keyboard()
            )
            return SELECTING_MODULE

    return ASKING_BANK


async def handle_branch_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle branch selection from callback."""
    query: CallbackQuery = update.callback_query
    user_id = update.effective_user.id
    session = get_user_session(user_id)

    await query.answer()

    if query.data == "back_main":
        session["state"] = SELECTING_MODULE
        session["data"] = {}
        session["module"] = None
        await query.edit_message_text(
            "╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗\n"
            "║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝\n"
            "╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═\n"
            "   HACKER TERMINAL v3.3.3\n\n"
            "📱 TELEGRAM BOT INTERFACE\n"
            "📞 DATABASE MODULES ONLY\n\n"
            "Select a module to begin:",
            reply_markup=get_main_keyboard()
        )
        return SELECTING_MODULE

    if query.data == "back_bank":
        session["state"] = ASKING_BANK
        await query.edit_message_text(
            "Select a bank:",
            reply_markup=get_bank_selection_keyboard()
        )
        return ASKING_BANK

    if query.data.startswith("state_"):
        branch_mode = query.data.split("_")[1]
        session["data"]["branch_mode"] = branch_mode
        session["state"] = PROCESSING

        module_num = session.get("module", 1)
        count = session["data"].get("count", 10)
        ui = session["ui"]
        handlers = session["handlers"]
        handlers.user_branch_mode = branch_mode
        handlers.user_selected_state = branch_mode if branch_mode != "RANDOM" else None

        if module_num == 1:
            bank = {"name": "American First Credit Union", "routing": "021407913", "swift": "AFCUUS33"}
            handlers.user_count = count

            await query.edit_message_text(
                f"✅ Bank: {bank['name']}\n"
                f"✅ Branch: {branch_mode}\n\n"
                f"🔄 Generating {count} records...\n"
                f"Please wait...",
                reply_markup=get_back_keyboard()
            )

            try:
                ui.telegram_messages = []
                handlers.handle_option_1()

                if hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file):
                    results_filepath = handlers.last_results_file
                    results_filename = os.path.basename(results_filepath)
                else:
                    output_lines = ui.telegram_messages
                    results_text = "\n".join(output_lines) if output_lines else f"American First Credit Union - {count} records generated"
                    timestamp = main.get_timestamp().replace(":", "-").replace(" ", "_")
                    results_filename = f"American_First_Credit_Union_{timestamp}.txt"
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                        f.write(results_text)
                        results_filepath = f.name

                await query.edit_message_text(
                    f"✅ [COMPLETE] American First Credit Union\n\n"
                    f"Generated: {count} records\n"
                    f"Status: Success\n\n"
                    f"📥 Results preview and download below:",
                    reply_markup=get_back_keyboard()
                )

                try:
                    with open(results_filepath, 'r', encoding='utf-8') as f:
                        results_content = f.read()
                except Exception:
                    results_content = None

                if results_content:
                    preview = results_content[:3000]
                    if len(results_content) > 3000:
                        preview += "\n\n... (truncated, see full file below)"
                    try:
                        await query.message.reply_text(
                            f"📋 Results:\n\n{preview}",
                            reply_markup=get_back_keyboard()
                        )
                    except Exception:
                        pass

                try:
                    with open(results_filepath, 'rb') as f:
                        await query.message.reply_document(
                            document=InputFile(f, filename=results_filename),
                            caption=f"📄 American First Credit Union - {count} records - Full results",
                            reply_markup=get_back_keyboard()
                        )
                except Exception as e:
                    logger.error(f"Could not send file: {e}", exc_info=True)
                    await query.message.reply_text(
                        f"❌ Could not send file. Results saved at:\n{results_filepath}",
                        reply_markup=get_back_keyboard()
                    )

                if not (hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file)):
                    try:
                        os.unlink(results_filepath)
                    except Exception:
                        pass

                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
            except Exception as e:
                logger.error(f"Error processing Module 1: {e}", exc_info=True)
                await query.edit_message_text(
                    f"❌ [HACKER ERROR] {str(e)}\n\n"
                    f"Use /start to return to main menu.",
                    reply_markup=get_main_keyboard()
                )
                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
        elif module_num == 3:
            bank_idx = session["data"].get("bank_idx", 0)
            bank = main.US_BANKS[bank_idx] if bank_idx < len(main.US_BANKS) else main.US_BANKS[0]
            handlers.selected_bank = bank
            handlers.user_count = count
            handlers.user_institution = None

            await query.edit_message_text(
                f"✅ Bank: {bank['name']}\n"
                f"✅ Branch: {branch_mode}\n\n"
                f"🔄 Generating {count} records...\n"
                f"Please wait...",
                reply_markup=get_back_keyboard()
            )

            try:
                ui.telegram_messages = []
                handlers.handle_option_3()

                if hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file):
                    results_filepath = handlers.last_results_file
                    results_filename = os.path.basename(results_filepath)
                else:
                    output_lines = ui.telegram_messages
                    results_text = "\n".join(output_lines) if output_lines else f"USA Banks Database - {count} records generated"
                    timestamp = main.get_timestamp().replace(":", "-").replace(" ", "_")
                    results_filename = f"USA_Banks_Database_{timestamp}.txt"
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                        f.write(results_text)
                        results_filepath = f.name

                await query.edit_message_text(
                    f"✅ [COMPLETE] USA Banks Database\n\n"
                    f"Bank: {bank['name']}\n"
                    f"Generated: {count} records\n"
                    f"Status: Success\n\n"
                    f"📥 Results preview and download below:",
                    reply_markup=get_back_keyboard()
                )

                try:
                    with open(results_filepath, 'r', encoding='utf-8') as f:
                        results_content = f.read()
                except Exception:
                    results_content = None

                if results_content:
                    preview = results_content[:3000]
                    if len(results_content) > 3000:
                        preview += "\n\n... (truncated, see full file below)"
                    try:
                        await query.message.reply_text(
                            f"📋 Results:\n\n{preview}",
                            reply_markup=get_back_keyboard()
                        )
                    except Exception:
                        pass

                try:
                    with open(results_filepath, 'rb') as f:
                        await query.message.reply_document(
                            document=InputFile(f, filename=results_filename),
                            caption=f"📄 USA Banks Database - {count} records - Full results",
                            reply_markup=get_back_keyboard()
                        )
                except Exception as e:
                    logger.error(f"Could not send file: {e}", exc_info=True)
                    await query.message.reply_text(
                        f"❌ Could not send file. Results saved at:\n{results_filepath}",
                        reply_markup=get_back_keyboard()
                    )

                if not (hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file)):
                    try:
                        os.unlink(results_filepath)
                    except Exception:
                        pass

                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
            except Exception as e:
                logger.error(f"Error processing Module 3: {e}", exc_info=True)
                await query.edit_message_text(
                    f"❌ [HACKER ERROR] {str(e)}\n\n"
                    f"Use /start to return to main menu.",
                    reply_markup=get_main_keyboard()
                )
                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
        elif module_num == 4:
            inst_idx = session["data"].get("inst_idx", 0)
            institutions = [
                {"name": "Royal Bank of Canada", "inst": "003", "transit": "12345"},
                {"name": "Toronto-Dominion Bank", "inst": "004", "transit": "23456"},
                {"name": "Scotiabank", "inst": "002", "transit": "34567"},
                {"name": "Bank of Montreal", "inst": "001", "transit": "45678"},
                {"name": "CIBC", "inst": "010", "transit": "56789"},
            ]
            inst = institutions[inst_idx] if inst_idx < len(institutions) else institutions[0]
            handlers.user_institution = inst_idx
            handlers.selected_bank = None
            handlers.user_count = count

            await query.edit_message_text(
                f"✅ Institution: {inst['name']}\n"
                f"✅ Branch: {branch_mode}\n\n"
                f"🔄 Generating {count} records...\n"
                f"Please wait...",
                reply_markup=get_back_keyboard()
            )

            try:
                ui.telegram_messages = []
                handlers.handle_option_4()

                if hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file):
                    results_filepath = handlers.last_results_file
                    results_filename = os.path.basename(results_filepath)
                else:
                    output_lines = ui.telegram_messages
                    results_text = "\n".join(output_lines) if output_lines else f"Canada Banks Database - {count} records generated"
                    timestamp = main.get_timestamp().replace(":", "-").replace(" ", "_")
                    results_filename = f"Canada_Banks_Database_{timestamp}.txt"
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                        f.write(results_text)
                        results_filepath = f.name

                await query.edit_message_text(
                    f"✅ [COMPLETE] Canada Banks Database\n\n"
                    f"Institution: {inst['name']}\n"
                    f"Generated: {count} records\n"
                    f"Status: Success\n\n"
                    f"📥 Results preview and download below:",
                    reply_markup=get_back_keyboard()
                )

                try:
                    with open(results_filepath, 'r', encoding='utf-8') as f:
                        results_content = f.read()
                except Exception:
                    results_content = None

                if results_content:
                    preview = results_content[:3000]
                    if len(results_content) > 3000:
                        preview += "\n\n... (truncated, see full file below)"
                    try:
                        await query.message.reply_text(
                            f"📋 Results:\n\n{preview}",
                            reply_markup=get_back_keyboard()
                        )
                    except Exception:
                        pass

                try:
                    with open(results_filepath, 'rb') as f:
                        await query.message.reply_document(
                            document=InputFile(f, filename=results_filename),
                            caption=f"📄 Canada Banks Database - {count} records - Full results",
                            reply_markup=get_back_keyboard()
                        )
                except Exception as e:
                    logger.error(f"Could not send file: {e}", exc_info=True)
                    await query.message.reply_text(
                        f"❌ Could not send file. Results saved at:\n{results_filepath}",
                        reply_markup=get_back_keyboard()
                    )

                if not (hasattr(handlers, 'last_results_file') and handlers.last_results_file and os.path.exists(handlers.last_results_file)):
                    try:
                        os.unlink(results_filepath)
                    except Exception:
                        pass

                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
            except Exception as e:
                logger.error(f"Error processing Module 4: {e}", exc_info=True)
                await query.edit_message_text(
                    f"❌ [HACKER ERROR] {str(e)}\n\n"
                    f"Use /start to return to main menu.",
                    reply_markup=get_main_keyboard()
                )
                session["state"] = SELECTING_MODULE
                return SELECTING_MODULE
        else:
            await query.edit_message_text(
                f"✅ Bank: American First Credit Union\n"
                f"✅ Branch: {branch_mode}\n\n"
                f"🔄 Generating {count} records...\n"
                f"Please wait...",
                reply_markup=get_back_keyboard()
            )
            session["state"] = SELECTING_MODULE
            return SELECTING_MODULE

    return ASKING_BRANCH


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current operation."""
    user_id = update.effective_user.id
    session = get_user_session(user_id)
    session["state"] = SELECTING_MODULE
    session["data"] = {}
    session["module"] = None

    await update.message.reply_text(
        "✅ [SUCCESS] Operation cancelled.\n\n"
        "Use /start to return to main menu.",
        reply_markup=get_main_keyboard()
    )
    return SELECTING_MODULE


def main_telegram() -> None:
    """Start the Telegram bot."""
    print("╔╦╗╔═╗╦═╗╦╔═╗╦ ╦╦  ╦╔═╗╦═╗")
    print("║║║║╣ ╠╦╝║╠═╝║ ║╚╗╔╝║╣ ╠╦╝")
    print("╩ ╩╚═╝╩╚═╩╩  ╚═╝ ╚╝ ╚═╝╩╚═")
    print("   HACKER TERMINAL v3.3.3")
    print()
    print("🤖 TELEGRAM BOT INTERFACE")
    print(f"🔑 Token: {BOT_TOKEN[:10]}...")
    print()
    print("Starting bot...")

    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            SELECTING_MODULE: [
                CallbackQueryHandler(button_callback),
            ],
            ASKING_COUNT: [
                MessageHandler(None, handle_count_input),
                CallbackQueryHandler(button_callback),
            ],
            ASKING_BANK: [
                CallbackQueryHandler(button_callback),
                CallbackQueryHandler(handle_bank_selection),
            ],
            ASKING_BRANCH: [
                CallbackQueryHandler(handle_branch_selection),
            ],
            PROCESSING: [
                CallbackQueryHandler(button_callback),
            ],
            DOWNLOADING: [
                CallbackQueryHandler(button_callback),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CommandHandler("cancel", cancel_command),
        ],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)

    # Start bot
    print("✅ Bot started successfully!")
    print("📱 Open Telegram and send /start to your bot")
    print("Press Ctrl+C to stop")

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n\n✅ Bot stopped gracefully")


if __name__ == "__main__":
    main_telegram()

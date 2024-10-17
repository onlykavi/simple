import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

TOKEN = '7792992988:AAFFoy686vjVe6i51YGv0bRDxkHc-nlmtoY'

tournaments = {}
users = {}
promoted_users = []
admins = ['1282074873', '5816482345', '6265981509']  # Replace with your admin IDs

def start(update, context):
    context.bot.send_message(chat_id=(update_effective_chat_id), text='Welcome to Tournament Manager!')

def help(update, context):
    context.bot.send_message(chat_id=(update_effective_chat_id), text='''
    Available commands:
    /start - Welcome message
    /help - List of available commands
    /create_tournament - Create a new tournament (Promoted users only)
    /join_tournament - Join an existing tournament
    /leave_tournament - Leave a tournament
    /matchups - Generate random matchups (Admins only)
    /broadcast - Send a broadcast message to all participants (Admins only)
    /title - Set a title for the tournament (Admins only)
    /participants - List all participants
    /start_tournament - Start the tournament
    /group_link - Get the group link
    /entry_fee - Get the entry fee information
    /min_players - Set the minimum number of players required (Admins only)
    /max_players - Set the maximum number of players allowed (Admins only)
    /give_title - Give a title to a user (Admins only)
    /check_title - Check user's title
    /promote_user - Promote a user (Admins only)
    /demote_user - Demote a user (Admins only)
    /auction_bid - Place an auction bid (Players only)
    /choose_captain - Choose a captain (Admins only)
    ''')

def create_tournament(update, context):
    # Create a new tournament (Promoted users only)
    if (update_effective_user_id) in promoted_users:
        tournament_id = len(tournaments) + 1
        tournaments[tournament_id] = {
            'title': '',
            'description': '',
            'min_players': 2,
            'max_players': 10,
            'participants': [],
            'entry_fee': '',
            'group_link': 'https://t.me/phg_tours'
        }
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Tournament {tournament_id} created!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only promoted users can create tournaments!')

def join_tournament(update, context):
    # Join an existing tournament
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        if len(tournaments[tournament_id]['participants']) < tournaments[tournament_id]['max_players']:
            tournaments[tournament_id]['participants'].append((update_effective_user_id))
            context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Joined tournament {tournament_id}!')
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament is full!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def leave_tournament(update, context):
    # Leave a tournament
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        tournaments[tournament_id]['participants'].remove((update_effective_user_id))
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Left tournament {tournament_id}!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def matchups(update, context):
    # Generate random matchups (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        if tournament_id in tournaments:
            participants = tournaments[tournament_id]['participants']
            matchups = []
            for i in range(len(participants) // 2):
                matchups.append((participants[i], participants[len(participants) - i - 1]))
            context.bot.send_message(chat_id=(update_effective_chat_id), text='\n'.join([f'{p1} vs {p2}' for p1, p2 in matchups]))
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can generate matchups!')

def broadcast(update, context):
    # Send a broadcast message to all participants (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        message = ' '.join(context.args[1:])
        if tournament_id in tournaments:
            for participant in tournaments[tournament_id]['participants']:context.bot.send_message(chat_id=participant, text=message)
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Broadcast sent!')
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can broadcast!')

def title(update, context):
    # Set a title for the tournament (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        title = ' '.join(context.args[1:])
        if tournament_id in tournaments:
            tournaments[tournament_id]['title'] = title
            context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Title updated for tournament {tournament_id}!')
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can set titles!')

def give_title(update, context):
    # Give a title to a user (Admins only)
    if (update_effective_user_id) in admins:
        user_id = int(context.args[0])
        title = ' '.join(context.args[1:])
        users[user_id] = {'title': title}
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Title given to user {user_id}!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can give titles!')

def check_title(update, context):
    # Check user's title
    user_id = (update_effective_user_id)
    if user_id in users:
        context.bot.send_message(chat_id=(update_effective_chat_id), text=users[user_id]['title'])
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='No title found!')

def promote_user(update, context):
    # Promote a user (Admins only)
    if (update_effective_user_id) in admins:
        user_id = int(context.args[0])
        promoted_users.append(user_id)
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'User {user_id} promoted!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can promote users!')

def demote_user(update, context):
    # Demote a user (Admins only)
    if (update_effective_user_id) in admins:
        user_id = int(context.args[0])
        promoted_users.remove(user_id)
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'User {user_id} demoted!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can demote users!')

def auction_bid(update, context):
    # Place an auction bid (Players only)
    tournament_id = int(context.args[0])
    bid = int(context.args[1])
    if tournament_id in tournaments and bid <= 100:
        # Update bid in tournament data
        pass
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Invalid bid!')

def choose_captain(update, context):
    # Choose a captain (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        captain_id = int(context.args[1])
        # Update captain in tournament data
        pass
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can choose captains!')

def group_link(update, context):
    # Get the group link
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        context.bot.send_message(chat_id=(update_effective_chat_id), text=tournaments[tournament_id]['group_link'])
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def entry_fee(update, context):
    # Get the entry fee information
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        context.bot.send_message(chat_id=(update_effective_chat_id), text=tournaments[tournament_id]['entry_fee'])
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def min_players(update, context):
    # Set the minimum number of players required (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        min_players = int(context.args[1])
        if tournament_id in tournaments:
            tournaments[tournament_id]['min_players'] = min_players
            context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Minimum players updated to {min_players} for tournament {tournament_id}!')
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can set minimum players!')

def max_players(update, context):
    # Set the maximum number of players allowed (Admins only)
    if (update_effective_user_id) in admins:
        tournament_id = int(context.args[0])
        max_players = int(context.args[1])
        if tournament_id in tournaments:
            tournaments[tournament_id]['max_players'] = max_players
            context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Maximum players updated to {max_players} for tournament {tournament_id}!')
        else:
            context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Only admins can set maximum players!')

def participants(update, context):
    # List all participants
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        participants = tournaments[tournament_id]['participants']
        context.bot.send_message(chat_id=(update_effective_chat_id), text='\n'.join(participants))
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def start_tournament(update, context):
    # Start the tournament
    tournament_id = int(context.args[0])
    if tournament_id in tournaments:
        context.bot.send_message(chat_id=(update_effective_chat_id), text=f'Tournament {tournament_id} started!')
    else:
        context.bot.send_message(chat_id=(update_effective_chat_id), text='Tournament not found!')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('create_tournament', create_tournament))
    dp.add_handler(CommandHandler('join_tournament', join_tournament))
    dp.add_handler(CommandHandler('leave_tournament', leave_tournament))
    dp.add_handler(CommandHandler('matchups', matchups))
    dp.add_handler(CommandHandler('broadcast', broadcast))
    dp.add_handler(CommandHandler('title', title))
    dp.add_handler(CommandHandler('give_title', give_title))
    dp.add_handler(CommandHandler('check_title', check_title))
    dp.add_handler(CommandHandler('promote_user', promote_user))
    dp.add_handler(CommandHandler('demote_user', demote_user))
    dp.add_handler(CommandHandler('auction_bid', auction_bid))
    dp.add_handler(CommandHandler('choose_captain', choose_captain))
    dp.add_handler(CommandHandler('group_link', group_link))
    dp.add_handler(CommandHandler('entry_fee', entry_fee))
    dp.add_handler(CommandHandler('min_players', min_players))
    dp.add_handler(CommandHandler('max_players', max_players))
    dp.add_handler(CommandHandler('participants', participants))
    dp.add_handler(CommandHandler('start_tournament', start_tournament))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

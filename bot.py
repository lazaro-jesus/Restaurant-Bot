import asyncio
import aiohttp
import logging

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery, ForceReply
from models import(
    Client,
    Buttons,
    Order,
    Product
)

import services


# API_TOKEN = 'API_BOT_TOKEN'
API_TOKEN = 'API_BOT_TOKEN'

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar el bot
bot = AsyncTeleBot(API_TOKEN)
# Inicializar el session
session = aiohttp.ClientSession()
# Menu Buttons
buttons = Buttons()
# DataBase
Client.check_db()
Order.check_db()


# Manejador del comando /start
@bot.message_handler(commands=['start'], chat_types='private')
async def start(message: Message):
    # Comprobar cliente en base de datos
    client = Client(message)
    
    if client.created:
        # Comprobar si el cliente ya está registrado
        client_data = await services.client_exists(client.chat_id)
        
        if not client_data:
            client_data = await services.client_create(client.to_json)
            
        client.update(client_data)
            
    # Mostrar el menú inline al usuario
    await bot.send_message(client.chat_id, 'Bienvenido! Elige una opción:', reply_markup=buttons.main())

    
@bot.message_handler(func=lambda message: True, chat_types='private')
async def direction(message: Message):
    if not message.reply_to_message:
        return
    
    if message.reply_to_message.text != 'Ingrese su direccón de entrega:' \
        or not message.reply_to_message.from_user.is_bot:
            return
        
    chat_id = message.chat.id
    markup = Buttons()
    direction = message.text
    client = Client(message).get_pk()
    order = Order(client).read()
    
    body = order.to_send
    body['direction'] = direction

    await services.order_create(body)
    
    await bot.delete_message(chat_id, message.reply_to_message.id)
    await bot.send_message(chat_id, '✅ Órden enviada con éxito', reply_markup=markup.main())
    
    logger.info(f'@{message.from_user.username} ({order.chat_id}) make order made the order ({order.id})')
    order.delete()


# Manejador de la selección del menú
@bot.callback_query_handler(func=lambda call: True)
async def handle_menu_selection(call: CallbackQuery):
    chat_id = call.from_user.id
    message = call.message
    message_id = message.id
    data = call.data
    
    if data == 'restaurants':
        # Listar los restaurantes
        restaurants_data = await services.restaurant_list()
        await bot.edit_message_text(
            text='Elige un restaurante:',
            chat_id=chat_id, 
            message_id=message_id,
            reply_markup=buttons.restaurants(restaurants_data)
        )

    elif data.startswith('restaurant_'):
        # Obtener el identificador del restaurante
        restaurant_pk = int(data.split('_')[1])
        menu_data = await services.restaurant_menu(restaurant_pk)
        restaurant_name, keyboard = buttons.restaurant_menu(menu_data)
        
        await bot.edit_message_text(
            text=restaurant_name,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
            )
        
    elif data.startswith('order_'):
        # Obtener el identificador del producto
        product = Product(data.split('_')[1:])
        client = Client(message).get_pk()
        order = Order(client)
        order.add_product(product)
        
        await bot.answer_callback_query(
            callback_query_id=call.id,
            text=f'✅ {product.name} a la orden!',
            show_alert=True
            )
        
    elif data.startswith('delete_'):
        # Obtener el identificador del producto\
        product_id = int(data.split('_')[1])
        client = Client(message).get_pk()
        order = Order(client).read()
        order.delete_product(product_id)
        keyboard = Buttons()

        await bot.edit_message_text(
            text='📄 Órdenes',
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard.orders(order)
            )
        
    elif data == 'orders':
        client = Client(message).get_pk()
        order = Order(client).read()
        keyboard = Buttons()
        
        await bot.edit_message_text(
            text='📄 Órdenes',
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard.orders(order)
            )
        
        
        
    elif data == 'server_orders':
        client = Client(message).get_pk()
        orders = await services.order_list(client.pk)
        keyboard = Buttons()
        text = ''
        
        if not orders:
            await bot.answer_callback_query(
            callback_query_id=call.id,
            text='⁉️ Lo siento. No exiten órdenes suyas.',
            show_alert=True
            )
            return
        
        for order in orders:
            text += f'Orden ID: {order["order_id"]}\n'
            text += f'Dirección: {order["direction"]}\nProductos:\n'
            for product in order['products']:
                text += f'{product["description"]} - {product["price"]}CUP\n'
            text += '\n'
        
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard.statics()
            )
    
    elif data == 'send':
        client = Client(message).get_pk()
        order = Order(client).read()
        
        if len(order.products) < 1:
            return
        
        await bot.send_message(
            text='Ingrese su direccón de entrega:',
            chat_id=chat_id,
            reply_markup=ForceReply()
            )
        
    elif data == '_':
        return
    
    else:
        await bot.edit_message_text(
                text='Bienvenido! Elige una opción:',
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=buttons.main()
                )

    
if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())
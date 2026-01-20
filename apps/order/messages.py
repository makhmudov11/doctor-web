ORDER_CREATED_TITLE = "Order #{order_id} muvaffaqiyatli yaratildi"
ORDER_CREATED_BODY = "Sizning orderingiz #{order_id} processing holatda"
ORDER_PAID_TITLE = "Order #{order_id} muvaffaqiyatli to‘landi"
ORDER_PAID_BODY = "Sizning orderingiz #{order_id} statusi: {status}"

ORDER_MESSAGES = {
    'created': {
        'title': "🛒 Buyurtma yaratildi",
        'body': "Sizning buyurtmangiz muvaffaqiyatli yaratildi. ID: {order_id}"
    },
    'accepted': {
        'title': "✅ Buyurtma qabul qilindi",
        'body': "Buyurtma #{order_id} shifokor tomonidan qabul qilindi"
    },
    'canceled': {
        'title': "❌ Buyurtma bekor qilindi",
        'body': "Buyurtma #{order_id} bekor qilindi"
    }
}

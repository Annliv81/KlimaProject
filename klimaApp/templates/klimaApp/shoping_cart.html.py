{% extends 'base.html' %}
{% block content %}

koszyk : <br>
{%for item in cart.cartproduct_set.all %}
    <p>{{item.produkt.name}}{{item.product.price}}{{item.quantity}}</p>

{% endfor %}

{% endblock %}
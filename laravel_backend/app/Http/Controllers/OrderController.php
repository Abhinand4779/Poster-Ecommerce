<?php

namespace App\Http\Controllers;

use App\Models\Order;
use Illuminate\Http\Request;

class OrderController extends Controller
{
    // List all orders for Admin
    public function index()
    {
        return response()->json(Order::latest()->get());
    }

    // Save a new order from Checkout
    public function store(Request $request)
    {
        $validated = $request->validate([
            'customer_name' => 'required|string',
            'customer_email' => 'required|email',
            'phone' => 'required|string',
            'address' => 'required|string',
            'total_amount' => 'required|numeric',
            'items' => 'required|array'
        ]);

        $validated['order_number'] = 'ORD-' . strtoupper(uniqid());
        $order = Order::create($validated);

        return response()->json(['message' => 'Order placed!', 'order_number' => $order->order_number], 201);
    }
}

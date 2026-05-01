<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\Request;

class ProductController extends Controller
{
    // Fetch products for the user side
    public function index(Request $request)
    {
        $category = $request->query('category');
        $query = Product::query();

        if ($category && $category !== 'all') {
            $query->where('category', 'like', $category);
        }

        return response()->json($query->latest()->get());
    }

    // Add a new product from Admin
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string',
            'category' => 'required|string',
            'price' => 'required|numeric',
            'image' => 'required|string',
        ]);

        $product = Product::create($validated);
        return response()->json([
            'message' => 'Product created successfully!', 
            'product' => $product
        ], 201);
    }

    // Update an existing product
    public function update(Request $request, $id)
    {
        $product = Product::findOrFail($id);
        
        $validated = $request->validate([
            'name' => 'sometimes|required|string',
            'category' => 'sometimes|required|string',
            'price' => 'sometimes|required|numeric',
            'image' => 'sometimes|required|string',
        ]);

        $product->update($validated);
        return response()->json([
            'message' => 'Product updated successfully!',
            'product' => $product
        ]);
    }

    // Delete a product
    public function destroy($id)
    {
        $product = Product::findOrFail($id);
        $product->delete();
        return response()->json(['message' => 'Product deleted successfully!']);
    }
}

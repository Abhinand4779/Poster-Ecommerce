<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\SettingsController;

/*
|--------------------------------------------------------------------------
| API Routes for Klaiz Designs
|--------------------------------------------------------------------------
*/

// Public Routes (Used by your HTML/JS frontend)
Route::get('/products', [ProductController::class, 'index']);
Route::get('/settings/{key}', [SettingsController::class, 'show']);
Route::post('/orders', [OrderController::class, 'store']);

// Admin Routes (Used by your Admin Dashboard)
Route::prefix('admin')->group(function () {
    Route::post('/products', [ProductController::class, 'store']);
    Route::put('/products/{id}', [ProductController::class, 'update']);
    Route::delete('/products/{id}', [ProductController::class, 'destroy']);
    
    Route::get('/orders', [OrderController::class, 'index']);
    Route::put('/orders/{id}/status', [OrderController::class, 'updateStatus']);
    
    Route::post('/settings', [SettingsController::class, 'update']);
});

<?php

namespace App\Http\Controllers;

use App\Models\Setting;
use Illuminate\Http\Request;

class SettingsController extends Controller
{
    // Get a specific setting (like 'marquee_text')
    public function show($key)
    {
        $setting = Setting::where('key', $key)->first();
        return response()->json($setting ? ['value' => $setting->value] : ['value' => '']);
    }

    // Update a setting from Admin
    public function update(Request $request)
    {
        $validated = $request->validate([
            'key' => 'required|string',
            'value' => 'required|string'
        ]);

        $setting = Setting::updateOrCreate(
            ['key' => $validated['key']],
            ['value' => $validated['value']]
        );

        return response()->json(['message' => 'Setting updated!']);
    }
}

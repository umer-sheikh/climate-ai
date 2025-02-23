<?php

use App\Http\Controllers\Auth\RegisteredUserController;
use App\Http\Controllers\VendorController;
use Illuminate\Support\Facades\Route;
use App\Models\Vendor;
use Illuminate\Support\Facades\Http;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return redirect()->route('login');
});

Route::get('/mbzuai-climate-ai', [VendorController::class, 'ai'])->middleware(['auth', 'verified'])->name('dashboard');
Route::get('/mbzuai-mcq', [VendorController::class, 'mcq'])->middleware(['auth', 'verified'])->name('mcq');
Route::get('/mbzuai-live-agent', [VendorController::class, 'live_agent'])->middleware(['auth', 'verified'])->name('live_agent');
Route::get('/vlm', [VendorController::class, 'vlm'])->middleware(['auth', 'verified'])->name('vlm');
Route::post('/mw-vendors-ai-msg', [VendorController::class, 'get_response'])->name('vendors.get_response');
Route::get('/gen-ai-article', [VendorController::class, 'gen_ai_article'])->name('vendors.gen_ai_article');

Route::get('/update-profile', [RegisteredUserController::class, 'edit'])->middleware('auth')->name('update-profile');
Route::post('/update-profile', [RegisteredUserController::class, 'update'])->middleware('auth');

Route::get('/test', function () {
    $payload = [
        "api_key" => "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",
        "query" => "",
        "search_depth" => "basic",
        "include_answer" => true,
        "include_images" => false,
        "include_image_descriptions" => false,
        "include_raw_content" => false,
        "max_results" => 5,
        "include_domains" => [],
        "exclude_domains" => []
    ];

    // Make the API request
    $response = Http::withHeaders([
        'Content-Type' => 'application/json',
    ])->post('https://api.tavily.com/search', $payload);

    $responseBody = json_decode($response->getBody(), true);

    dd($responseBody['answer']);
});

require __DIR__.'/auth.php';

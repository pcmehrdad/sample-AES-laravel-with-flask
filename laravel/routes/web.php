<?php

use Illuminate\Support\Facades\Route;

Route::get('/encrypt', [\App\Http\Controllers\TestController::class,'encrypt']);
Route::get('/decrypt', [\App\Http\Controllers\TestController::class,'decrypt']);


<?php

namespace App\Http\Controllers;

use App\Models\Vendor;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Parsedown;

use function PHPSTORM_META\type;

class VendorController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view('vendors-create');
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $logo = $request->file('logo');
        $logo->move('assets/img/vendors', $logo->getClientOriginalName());
        //store path in var
        $path = 'assets/img/vendors/' . $logo->getClientOriginalName();

        // create new vendor
        $vendor = new Vendor;
        $vendor->name = $request->name;
        $vendor->logo_path = $path;
        $vendor->tech = $request->tech;
        $vendor->coverage = $request->coverage;
        $vendor->current_distribution = $request->current_distribution;
        $vendor->competition = $request->competition;
        //revenue forecast is json
        $rev = [
            '2025' => $request->revenue_1,
            '2026' => $request->revenue_2,
            '2027' => $request->revenue_3,
            '2028' => $request->revenue_4,
        ];
        $vendor->revenue_forecast = json_encode($rev);
        $vendor->nda = $request->nda;
        $vendor->mp = $request->mp;
        $vendor->e_comm = $request->e_comm;
        $vendor->comments = $request->comments;
        $vendor->status = $request->status;
        $vendor->initiated_by = $request->initiated_by;
        $vendor->contact_at_vendor = $request->contact_at_vendor;
        $vendor->website = $request->website;
        $vendor->overview = $request->overview;
        $vendor->user_id = auth()->user()->id;
        $vendor->save();

        return redirect()->route('dashboard');
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Vendor  $vendor
     * @return \Illuminate\Http\Response
     */
    public function show(Vendor $vendor)
    {
        return view('vendors-show', compact('vendor'));
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\Vendor  $vendor
     * @return \Illuminate\Http\Response
     */
    public function edit(Vendor $vendor)
    {
        return view('vendors-edit', compact('vendor'));
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Vendor  $vendor
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Vendor $vendor)
    {
        //
    }

    public function ai()
    {
        $topics = ['sand storm', 'rain', 'fog', 'hail', 'thunderstorm', 'tornado', 'hurricane', 'cyclone', 'heat wave', 'cold wave'];

        $payload = [
            'model' => 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens' => 840,
            'temperature' => 0.7,
            'top_p' => 0.7,
            'top_k' => 50,
            'repetition_penalty' => 1,
            'messages' => [
                [
                    'role' => 'user',
                    'content' => uniqid() . ' Give 4 titles (around 20 words) for UAE weather, return only titles separated by #. Response:'
                ]
            ]
        ];

        // Make the API request
        //get TOGETHER_API_KEY from env
        $api_key = env('TOGETHER_API_KEY');
        $response = Http::withHeaders([
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer '. $api_key
        ])->post('https://api.together.xyz/v1/chat/completions', $payload);

        $responseBody = json_decode($response->getBody(), true);

        // Extract the message content
        $messageContent = $responseBody['choices'][0]['message']['content'];

        $titles = explode('#', $messageContent);

        return view('vendors-ai', compact('titles'));
    }

    public function mcq()
    {
        return view('mcqs');
    }

    public function vlm()
    {
        return view('vlm');
    }

    public function live_agent()
    {
        return view('live-agent');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Vendor  $vendor
     * @return \Illuminate\Http\Response
     */
    public function destroy(Vendor $vendor)
    {
        //
    }

    public function get_response(Request $request)
    {
        //
    }

    public function gen_ai_article(Request $request) {
        // get title from query str
        $topic = $request->query('topic');
        $topic = str_replace('-', ' ', $topic);

        $payload = [
            'model' => 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
            'max_tokens' => 840,
            'temperature' => 0.7,
            'top_p' => 0.7,
            'top_k' => 50,
            'repetition_penalty' => 1,
            'messages' => [
                [
                    'role' => 'user',
                    'content' => 'Generate an article on this topic: ' . $topic
                ]
            ]
        ];

        // Make the API request
        //get TOGETHER_API_KEY from env
        $api_key = env('TOGETHER_API_KEY');
        $response = Http::withHeaders([
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer '.$api_key
        ])->post('https://api.together.xyz/v1/chat/completions', $payload);

        $responseBody = json_decode($response->getBody(), true);

        // Extract the message content
        $messageContent = $responseBody['choices'][0]['message']['content'];

        // Return the message content
        $parsedResponse = (new Parsedown())->text($messageContent);

        return view('ai-article', compact('parsedResponse'));
    }

    public function get_live_response(Request $request)
    {
        //
    }
}

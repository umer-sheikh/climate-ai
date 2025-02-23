<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <section class="section">
        <div class="section-body">
            <div class="row">
                <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
                    <div class="card">
                        <div class="chat">
                            <div class="chat-header clearfix">
                                <img src="{{ asset('assets/img/ai.png') }}" alt="avatar">
                                <div class="chat-about">
                                    <div class="chat-with">MBZUAI Climate News</div>
                                    <div class="chat-num-messages">This blog is created using AI</div>
                                </div>
                            </div>
                            <div class="card-body">
                                {!! $parsedResponse !!}
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    </section>

    @section('js')
    @endsection
</x-app-layout>

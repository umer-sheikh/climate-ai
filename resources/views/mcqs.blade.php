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
                                    <div class="chat-with">MBZUAI Climate MCQs</div>
                                    <div class="chat-num-messages">An AI agent to answer queries related to UAE climate</div>
                                </div>
                            </div>
                        </div>
                        <div class="chat-box" id="mychatbox">
                            <div class="card-body chat-content">
                            </div>
                            <div class="card-footer chat-form">
                                <form id="chat-form">
                                    <input type="text" class="form-control" placeholder="Type a message">
                                    <button class="btn btn-primary">
                                        <i class="far fa-paper-plane"></i>
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    @section('js')
        <script src="assets/js/page/chat.js"></script>
        <script>
            let chat = [
                {
                    content: 'My name is MBZUAI MCQs AI. I will ask user about UAE specific climate MCQs. User can answer the questions. I will provide feedback on the answers. I will also provide the correct answer if user answer is wrong. I will also provide the score of user at the end of the quiz.',
                    role: 'system',
                },
            ];

            $("#chat-form").submit(function () {
                var me = $(this);
                
                if (me.find('input').val().trim().length > 0) {

                    let msg = me.find('input').val();
                    $.chatCtrl('#mychatbox', {
                    text: msg,
                    picture: 'assets/img/pj.jpeg',
                    });
                    // push user message
                    chat.push({
                        content: msg,
                        role: 'user',
                    });

                    typing_element = '<div class="chat-item chat-left chat-typing" style="display:none">' +
                    '<img src="assets/img/ai.png">' +
                    '<div class="chat-details">' +
                    '<div class="chat-text"></div>' +
                    '</div>' +
                    '</div>';
                    $('.chat-content').append($(typing_element).fadeIn())

                    //ajax call to /mw-vendors-ai-msg with chat data
                    $.ajax({
                        url: '/mw-vendors-ai-msg',
                        type: 'POST',
                        data: {
                            chat: chat,
                        },
                        success: function (response) {
                            // push AI response
                            chat.push({
                                content: response,
                                role: 'assistant',
                            });
                            $('.chat-typing').remove();
                            $.chatCtrl('#mychatbox', {
                                text: response,
                                picture: "assets/img/ai.png",
                                position: 'chat-left',
                                type: 'text'
                            });
                            console.log(response)
                        },
                    });

                    me.find('input').val('');
                }
                return false;
            });
        </script>
    @endsection
</x-app-layout>

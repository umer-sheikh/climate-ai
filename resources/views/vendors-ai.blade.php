<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            {{ __('Dashboard') }}
        </h2>
    </x-slot>

    <section class="section">
        <div class="section-body">
            <div class="row">
                <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
                    <div class="card">
                        <div class="chat">
                            <div class="chat-header clearfix">
                                <img src="{{ asset('assets/img/ai.png') }}" alt="avatar">
                                <div class="chat-about">
                                    <div class="chat-with">MBZUAI Climate AI</div>
                                    <div class="chat-num-messages">An AI agent to answer queries related to UAE climate</div>
                                </div>
                            </div>
                        </div>
                        <div class="chat-box" id="mychatbox">
                            <div class="card-body chat-content">
                            </div>
                            <div class="card-footer chat-form">
                                <form id="chat-form">
                                    <input type="file" class="d-none" name="" id="select_img">
                                    <input type="text" id="user_message" class="form-control" placeholder="Type a message">
                                    <i class="material-icons" style="position: absolute; top: 25%; right: 75px; cursor: pointer;" onclick="document.getElementById('select_img').click()">attach_file</i>
                                    <button class="btn btn-primary">
                                        <i class="far fa-paper-plane"></i>
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3">
                    <div class="card">
                        <div class="card-header">
                          <h4>Related Blogs</h4>
                        </div>
                        <div class="card-body">
                            <ul class="list-unstyled user-progress list-unstyled-border">
                                @foreach ($titles as $title)
                                    <li class="media">
                                        <a href="{{ route('vendors.gen_ai_article', ['topic' => str_replace(' ', '-', $title)]) }}">{{ $title }}</a>
                                    </li>
                                @endforeach
                                
                                
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    @section('js')
        <script src="assets/js/page/chat.js"></script>
        <script>
            const getBase64 = (file) => {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => resolve(reader.result);
                    reader.onerror = error => reject(error);
                });
            };
            
            let chat = [];

            $("#chat-form").submit(async function (e) {
                e.preventDefault();
                var me = $(this);
                
                if (me.find('#user_message').val().trim().length > 0) {

                    let msg = me.find('#user_message').val();
                    let fileInput = $('#select_img')[0];

                    // push user message
                    chat.push({
                        content: msg,
                        role: 'user',
                    });

                    let form_data = { // Convert the data to JSON string
                        chat: chat,
                    }


                    if (fileInput.files && fileInput.files[0]) {
                        var file = fileInput.files[0];

                        if (file.type.match('image.*')) {
                            var imageUrl = URL.createObjectURL(file);
                            $('#imageId').attr('src', imageUrl);
                            $.chatCtrl('#mychatbox', {
                                text: msg,
                                text_img: imageUrl,
                                picture: 'assets/img/pj.jpeg',
                            });

                            const base64Image = await getBase64(file);
                            // Add to form_data
                            form_data.image = base64Image;
                        }
                    }else{
                        $.chatCtrl('#mychatbox', {
                            text: msg,
                            picture: 'assets/img/pj.jpeg',
                        });
                    }


                    typing_element = '<div class="chat-item chat-left chat-typing" style="display:none">' +
                    '<img src="assets/img/ai.png">' +
                    '<div class="chat-details">' +
                    '<div class="chat-text"></div>' +
                    '</div>' +
                    '</div>';
                    $('.chat-content').append($(typing_element).fadeIn())

                    //ajax call to /mw-vendors-ai-msg with chat data
                    $.ajax({
                        url: 'http://localhost:5001/chat/completion',
                        type: 'POST',
                        contentType: 'application/json', // Specify that data is JSON
                        data: JSON.stringify(form_data),
                        success: function (response) {
                            console.log(response);
                            // push AI response
                            chat.push({
                                content: response.message,
                                role: 'assistant',
                            });
                            $('.chat-typing').remove();
                            let response_date = {
                                text: response.message,
                                picture: "assets/img/ai.png",
                                position: 'chat-left',
                                type: 'text'
                            }
                            if(response.annotated_image){
                                response_date.text_img = response.annotated_image;
                            }
                            $.chatCtrl('#mychatbox', response_date);
                        },
                    });

                    me.find('input').val('');
                }
                return false;
            });
        </script>
    @endsection
</x-app-layout>

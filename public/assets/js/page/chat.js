"use strict";

$.chatCtrl = function (element, chat) {
    try {
        var chat = $.extend(
            {
                position: "chat-right",
                text: "",
                text_img: "",
                time: moment(new Date().toISOString()).format("hh:mm"),
                picture: "",
                type: "text", // or typing
                timeout: 0,
                onShow: function () {},
            },
            chat
        );

        var target = $(element);
        let image_element = "";

        if (chat.text_img) {
            image_element =
                '<div style="height: 310px"><img src="' +
                chat.text_img +
                '" height="300" width="300"> <br></div>';
        }

        element =
            '<div class="chat-item ' +
            chat.position +
            '" style="display:none">' +
            '<img src="' +
            chat.picture +
            '">' +
            '<div class="chat-details">' +
            '<div class="chat-text">' +
            image_element +
            '<div>' + chat.text + '</div>' +
            "</div>" +
            '<div class="chat-time">' +
            chat.time +
            "</div>" +
            "</div>" +
            "</div>";

        // typing_element = '<div class="chat-item chat-left chat-typing" style="display:none">' +
        //   '<img src="' + chat.picture + '">' +
        //   '<div class="chat-details">' +
        //   '<div class="chat-text"></div>' +
        //   '</div>' +
        //   '</div>';

        var append_element = element;
        // if (chat.type == 'typing') {
        //   append_element = typing_element;
        // }

        if (chat.timeout > 0) {
            setTimeout(function () {
                target.find(".chat-content").append($(append_element).fadeIn());
            }, chat.timeout);
        } else {
            target.find(".chat-content").append($(append_element).fadeIn());
        }

        var target_height = 0;
        target.find(".chat-content .chat-item").each(function () {
            target_height += $(this).outerHeight();
        });
        setTimeout(function () {
            target.find(".chat-content").scrollTop(target_height, -1);
        }, 100);
        chat.onShow.call(this, append_element);
    } catch (error) {
        console.log(error);
    }
};

if ($("#chat-scroll").length) {
    $("#chat-scroll")
        .css({
            height: 450,
        })
        .niceScroll();
}

if ($(".chat-content").length) {
    $(".chat-content").niceScroll({
        cursoropacitymin: 0.3,
        cursoropacitymax: 0.8,
    });
    $(".chat-content")
        .getNiceScroll(0)
        .doScrollTop($(".chat-content").height());
}

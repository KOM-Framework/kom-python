class HTML:

    @staticmethod
    def network_statistic_attachment_template(external_path_to_har_file):
        style_str = '<style>@keyframes spin{to{ transform: rotate(1turn);}} .progress{position: relative;display: inline-block;width: 5em;height: 5em;margin: 0 .5em;font-size: 12px;text-indent: 999em;overflow: hidden;animation: spin 1s infinite steps(8);} .small.progress{font-size: 6px;} .large.progress{font-size: 24px;} .progress:before, .progress:after, .progress > div:before, .progress > div:after{content: "";position: absolute;top: 0;left: 2.25em;width: .5em;height: 1.5em;border-radius: .2em;background: lime;box-shadow: 0 3.5em lime; transform-origin: 50% 2.5em;} .progress:before{background: blue;} .progress:after{transform: rotate(-45deg);background: gray;} .progress > div:before{transform: rotate(-90deg);background: yellow;} .progress > div:after{transform: rotate(-135deg);background: green;} body{background-color: white;} h1{color: blue;} p{color: red;}</style>'
        html_string = '<!DOCTYPE HTML>\
                        <html>\
                        <head>\
                            <meta charset="utf-8">%s\
                            <script src="https://code.jquery.com/jquery-2.1.4.min.js" integrity="sha256-8WqyJLuWKRBVhxXIL1jBDD7SDxU936oZkCnxQbWwJVw=" crossorigin="anonymous"></script>\
                            <script>\
                                (function () {var har = document.createElement("script");har.src = "http://www.softwareishard.com/har/viewer/har.js";har.setAttribute("id", "har");har.setAttribute("async", "true");document.documentElement.firstChild.appendChild(har);})();\
                                $(window).load(function() { $(".se-pre-con").fadeOut("slow"); });\
                            </script>\
                        </head>\
                        <body>\
                            <div id="loader" class="se-pre-con"></div>\
                            <div class="har" data-har="%s" height="800px"></div>\
                        </body>\
                        </html>\
                        ' % (style_str, external_path_to_har_file)
        return html_string

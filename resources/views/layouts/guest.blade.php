<!DOCTYPE html>
<html lang="en">


<!-- auth-login.html  21 Nov 2019 03:49:32 GMT -->
<head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no" name="viewport">
  <title>{{ config('app.name', 'MBZUAI Climate AI') }}</title>
  <!-- General CSS Files -->
  <link rel="stylesheet" href="{{ asset("assets/css/app.min.css") }} ">
  <link rel="stylesheet" href="{{ asset("assets/bundles/bootstrap-social/bootstrap-social.css") }} ">
  <!-- Template CSS -->
  <link rel="stylesheet" href="{{ asset("assets/css/style.css") }} ">
  <link rel="stylesheet" href="{{ asset("assets/css/components.css") }} ">
  <!-- Custom style CSS -->
  <link rel="stylesheet" href="{{ asset("assets/css/custom.css") }} ">
  <link rel='shortcut icon' type='image/x-icon' href='{{ asset("assets/img/fv.ico") }}' />
</head>

<body>
  <div class="loader"></div>
  <div id="app">
    {{ $slot }}
  </div>
  <!-- General JS Scripts -->
  <script src="{{ asset("assets/js/app.min.js") }}"></script>
  <!-- JS Libraies -->
  <!-- Page Specific JS File -->
  <!-- Template JS File -->
  <script src="{{ asset("assets/js/scripts.js") }}"></script>
  <!-- Custom JS File -->
  <script src="{{ asset("assets/js/custom.js") }}"></script>
</body>


<!-- auth-login.html  21 Nov 2019 03:49:32 GMT -->
</html>
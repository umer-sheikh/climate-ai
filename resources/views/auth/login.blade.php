<x-guest-layout>
    <section class="section">
        <div class="container mt-5">
          <div class="text-center mb-5 pt-4"><img alt="image" src="https://upload.wikimedia.org/wikipedia/en/thumb/5/55/Mohamed_bin_Zayed_University_of_Artificial_Intelligence_logo.png/300px-Mohamed_bin_Zayed_University_of_Artificial_Intelligence_logo.png" style="height: 70px;" class="header-logo" /> <br> <h3 class="mt-4">MBZUAI Climate AI</h3></div>
          <div class="row">
            <div class="col-12 col-sm-8 offset-sm-2 col-md-6 offset-md-3 col-lg-6 offset-lg-3 col-xl-4 offset-xl-4">
              <div class="card card-primary">
                <div class="card-header">
                  <h4>Login</h4>
                </div>
                <div class="card-body">
                    <!-- Session Status -->
                    <x-auth-session-status class="mb-4" :status="session('status')" />

                    <!-- Validation Errors -->
                    <x-auth-validation-errors class="mb-4" :errors="$errors" />

                  <form method="POST" action="{{ route('login') }}">
                    @csrf
                    <div class="form-group">
                      <label for="email">Email</label>
                      <input id="email" class="form-control" type="email" name="email" value="{{ old('email') }}" required autofocus>
                      <div class="invalid-feedback">
                        Please fill in your email
                      </div>
                    </div>
                    <div class="form-group">
                      <div class="d-block">
                        <label for="password" class="control-label">Password</label>
                        @if (Route::has('password.request'))
                        <div class="float-right">
                          <a href="{{ route('password.request') }}" class="text-small">
                            Forgot Password?
                          </a>
                        </div>
                        @endif
                      </div>
                      <input id="password" type="password" class="form-control" name="password" required autocomplete="current-password">
                      <div class="invalid-feedback">
                        please fill in your password
                      </div>
                    </div>
                    <div class="form-group">
                      <div class="custom-control custom-checkbox">
                        <input type="checkbox" name="remember" class="custom-control-input" tabindex="3" id="remember-me">
                        <label class="custom-control-label" for="remember-me">Remember Me</label>
                      </div>
                    </div>
                    <div class="form-group">
                      <button type="submit" class="btn btn-primary btn-lg btn-block" tabindex="4">
                        Login
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
</x-guest-layout>

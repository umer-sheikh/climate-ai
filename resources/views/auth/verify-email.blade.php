<x-app-layout>
    <section class="section">
        <div class="section-body">
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header"><h4>Email Verification</h4></div>
                        <div class="card-body">
                            <p>
                                Thanks for signing up! Before getting started, could you verify your email address by clicking on the link we just emailed to you? If you didn't receive the email, we will gladly send you another.
                            </p>
                            @if (session('status') == 'verification-link-sent')
                            <div class="alert alert-success alert-dismissible show fade">
                                <div class="alert-body">
                                    <button class="close" data-dismiss="alert">
                                        <span>&times;</span>
                                    </button>
                                    A new verification link has been sent to the email address you provided during registration.
                                </div>
                            </div>
                            @endif
                            <form method="POST" action="{{ route('verification.send') }}">
                                @csrf
                
                                <div>
                                    <input type="submit" value="Resend Verification Email" class="btn btn-primary">
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</x-app-layout>

@props(['errors'])

@if ($errors->any())
    <div {{ $attributes->merge(['class' => 'alert alert-danger alert-dismissible show fade']) }}>
        <div class="alert-body">
            <button class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
            @foreach ($errors->all() as $error)
                {{ $error }} 
            @endforeach
        </div>
    </div>
@endif

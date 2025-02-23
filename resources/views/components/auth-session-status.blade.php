@props(['status'])

@if ($status)
    <div class="">
        
    </div>
    <div {{ $attributes->merge(['class' => 'alert alert-success alert-dismissible show fade']) }}>
        <div class="alert-body">
            <button class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
            {{ $status }}
        </div>
    </div>
@endif

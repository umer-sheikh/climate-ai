<aside id="sidebar-wrapper">
    <div class="sidebar-brand">
      <a href="{{ route('dashboard') }}"> <img alt="image" src="https://upload.wikimedia.org/wikipedia/en/thumb/5/55/Mohamed_bin_Zayed_University_of_Artificial_Intelligence_logo.png/300px-Mohamed_bin_Zayed_University_of_Artificial_Intelligence_logo.png" style="height: 35px;" class="header-logo" />
      </a>
    </div>
    <ul class="sidebar-menu">
      <li class="menu-header">Main</li>
      {{-- <li class="dropdown {{ request()->routeIs('dashboard')? 'active' : '' }}">
        <a href="{{ route('dashboard') }}" class="nav-link"><i data-feather="list"></i><span>Vendors</span></a>
      </li>
      <li class="dropdown {{ request()->routeIs('add-vendor')? 'active' : '' }}">
        <a href="{{ route('vendors.create') }}" class="nav-link"><i data-feather="plus"></i><span>Add Vendor</span></a>
      </li> --}}
      <li class="dropdown {{ request()->routeIs('add-vendor')? 'active' : '' }}">
        <a href="{{ route('dashboard') }}" class="nav-link"><i data-feather="gitlab"></i><span>Climate AI</span></a>
      </li>
      <li class="dropdown {{ request()->routeIs('add-vendor')? 'active' : '' }}">
        <a href="{{ route('mcq') }}" class="nav-link"><i data-feather="help-circle"></i><span>MCQs</span></a>
      </li>
      {{-- <li class="dropdown {{ request()->routeIs('add-vendor')? 'active' : '' }}">
        <a href="{{ route('live_agent') }}" class="nav-link"><i data-feather="user"></i><span>Prediction Agent</span></a>
      </li>
      <li class="dropdown {{ request()->routeIs('add-vendor')? 'active' : '' }}">
        <a href="{{ route('vlm') }}" class="nav-link"><i data-feather="image"></i><span>VLM Model</span></a>
      </li> --}}
    </ul>
  </aside>
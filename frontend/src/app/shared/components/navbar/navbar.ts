import { Component, output } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html'
})
export class Navbar {
  menuToggle = output<void>();
}

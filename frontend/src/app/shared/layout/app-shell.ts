import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Navbar } from '../components/navbar/navbar';
import { Sidebar } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-shell',
  imports: [RouterOutlet, Navbar, Sidebar],
  templateUrl: './app-shell.html'
})
export class AppShell {
  menuOpen = signal(false);
}

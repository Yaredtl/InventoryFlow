import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Spinner } from './shared/components/spinner/spinner';
import { ToastComponent } from './shared/components/toast/toast';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Spinner, ToastComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {}

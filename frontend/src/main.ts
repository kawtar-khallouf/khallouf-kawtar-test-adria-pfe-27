import {bootstrapApplication} from '@angular/platform-browser';
import {provideHttpClient,withInterceptors} from '@angular/common/http';
import {AppComponent} from './app.component';
import {initAuth,token} from './auth';
import {from,switchMap} from 'rxjs';
import {HttpInterceptorFn} from '@angular/common/http';
const bearerInterceptor: HttpInterceptorFn = (req, next) => from(token()).pipe(switchMap(t => next(t ? req.clone({setHeaders:{Authorization:'Bearer '+t}}) : req)));
initAuth().then(()=>bootstrapApplication(AppComponent,{providers:[provideHttpClient(withInterceptors([bearerInterceptor]))]}));

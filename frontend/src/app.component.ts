import {Component,OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {auth} from './auth';
interface Account {id:string;customerReference:string;status:string;currency:string;balance:number}
interface Transaction {id:string;accountId:string;amount:number;currency:string;merchantCategory:string;country:string;createdAt:string;transactionType:string}
@Component({selector:'app-root',standalone:true,imports:[CommonModule,FormsModule],templateUrl:'./app.component.html'})
export class AppComponent implements OnInit {
  api='http://localhost:8080';accounts:Account[]=[];transactions:Transaction[]=[];notice='';chatAnswer='';loading=false;
  newAccount={customerReference:'',currency:'EUR',balance:1000};
  transaction={accountId:'',amount:50,currency:'EUR',merchantCategory:'SHOPPING',country:'MA'};
  transfer={sourceId:'',destinationId:'',amount:25,currency:'EUR'};
  prompt='Donne-moi la liste des comptes';confirmWrites=false;
  constructor(private http:HttpClient){}
  ngOnInit(){this.refresh()}
  get loggedIn(){return !!auth.authenticated}
  get username(){return auth.tokenParsed?.['preferred_username']||'Mode local'}
  login(){auth.login()}
  logout(){auth.logout({redirectUri:'http://localhost:4200'})}
  private fail(e:any){this.notice= 'Erreur : '+(e?.error?.detail||e?.error?.message||e?.message||'Service indisponible')}
  refresh(){this.http.get<Account[]>(this.api+'/api/accounts').subscribe({next:a=>this.accounts=a,error:e=>this.fail(e)});
    this.http.get<Transaction[]>(this.api+'/api/transactions').subscribe({next:t=>this.transactions=t,error:e=>this.fail(e)});}
  open(){this.http.post(this.api+'/api/accounts',this.newAccount).subscribe({next:()=>{this.notice='Compte créé';this.refresh()},error:e=>this.fail(e)})}
  pay(){this.http.post(this.api+'/api/transactions',this.transaction).subscribe({next:()=>{this.notice='Transaction enregistrée';this.refresh()},error:e=>this.fail(e)})}
  sendTransfer(){this.http.post(this.api+'/api/transfers',this.transfer).subscribe({next:()=>{this.notice='Virement enregistré';this.refresh()},error:e=>this.fail(e)})}
  chat(){this.loading=true;this.http.post<{answer:string}>(this.api+'/api/chat',{message:this.prompt,confirmWrites:this.confirmWrites}).subscribe({next:r=>{this.chatAnswer=r.answer;this.loading=false},error:e=>{this.fail(e);this.loading=false}})}
  activeCount(){return this.accounts.filter(a=>a.status==='ACTIVE').length}
  short(id:string){return id.slice(0,8)}
}

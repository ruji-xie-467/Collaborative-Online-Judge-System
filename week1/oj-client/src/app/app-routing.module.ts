import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProblemListComponent } from './components/problem-list/problem-list.component';
import { ProblemDetailComponent } from './components/problem-detail/problem-detail.component';

const routes: Routes = [
  { path: "", redirectTo: "problems", pathMatch: "full" },
  { path: 'problems', component: ProblemListComponent },
  { path: 'problems/:id', component: ProblemDetailComponent },
  { path: '**', redirectTo: "problems"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

// can also be written as below
//export const AppRoutingModule = RouterModule.forRoot(routes);

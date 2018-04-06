import { Routes, RouterModule } from '@angular/router';
import { EditdistanceComponent } from "./editdistance/editdistance.component";
const MAINMENU_ROUTES: Routes = [
    //full : makes sure the path is absolute path
    { path: '', redirectTo: '/editdistance', pathMatch: 'full' },
    { path: 'editdistance', component: EditdistanceComponent },

];
export const CONST_ROUTING = RouterModule.forRoot(MAINMENU_ROUTES);

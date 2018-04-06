import { Component, OnInit } from '@angular/core';
import { SharedService } from "./../shared.service";
 
@Component({
  selector: 'app-editdistance',
  templateUrl: './editdistance.component.html',
  styles: []
 
})
export class EditdistanceComponent implements OnInit {
  id_str_a: string = "";
  id_str_b: string = "";
  op_editdist: string = "";
  constructor(private _sharedService: SharedService) {
  }
 
  ngOnInit() {
  }
 
  callEditdistanceService() { 
    this._sharedService.findEditDistance(this.id_str_a, this.id_str_b)
      .subscribe(
      lstresult => {  
        this.op_editdist = lstresult["edit_distance"];
      },
      error => {
        console.log("Error. The editdistance result JSON value is as follows:");
        console.log(error);
      }
      ); 
  }
}
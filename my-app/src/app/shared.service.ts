import { Injectable } from '@angular/core';
import { Http, Headers, Response, RequestOptions } from "@angular/http";
import 'rxjs/Rx';
import { Observable } from "rxjs";
 
@Injectable()
export class SharedService {
    editdistanceURL = "http://localhost:8000/editdistance/find-edit-distance/";
    constructor(private _http: Http) { }

    findEditDistance(str_a, str_b) { 
        let headers      = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options       = new RequestOptions({ headers: headers }); // Create a request option
        let bodyObj = {"first_string": str_a, "second_string": str_b};
        return this._http.put(this.editdistanceURL, JSON.stringify(bodyObj), options)
            .map(response => {
                { return response.json() };
            })
            .catch(error => Observable.throw(error.json()));
    }
} 
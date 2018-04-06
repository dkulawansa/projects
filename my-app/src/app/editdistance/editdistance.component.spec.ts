import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditdistanceComponent } from './editdistance.component';

describe('EditdistanceComponent', () => {
  let component: EditdistanceComponent;
  let fixture: ComponentFixture<EditdistanceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditdistanceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditdistanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

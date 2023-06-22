// Constructor function
class LR {
    constructor() {
      this.coef_ = 0;
      this.intercept_ = 0;
    }
  
    cost(x, y, w, b) {
      const m = x.length;
      var f_wb = 0;
      var cost = 0;
  
      for (let i = 0; i < m; i++) {
        f_wb = w * x[i] + b;
        cost += Math.pow(f_wb - y[i], 2);
      }
  
      const j_wb = cost / (2 * m);
      return j_wb;
    }
    
  
    gradient(x, y, w, b) {
      const m = x.length;
      let dj_dw = 0;
      let dj_db = 0;
  
      for (let i = 0; i < m; i++) {
        const f_wb = w * x[i] + b;
        const dj_dw_i = (f_wb - y[i]) * x[i];
        const dj_db_i = f_wb - y[i];
        dj_dw += dj_dw_i;
        dj_db += dj_db_i;
      }
  
      dj_dw = dj_dw / m;
      dj_db = dj_db / m;
      return [dj_dw, dj_db];
    }
  
    fit(X_values, y_values) {
      let b = 0;
      let w = 0;
      const alpha = 0.01;
      const iterations = 50;
  
      for (let i = 0; i < iterations; i++) {
        const [dj_dw, dj_db] = this.gradient(X_values, y_values, w, b);
  
        w = w - alpha * dj_dw;
        b = b - alpha * dj_db;
      }

      this.coef_ = w;
      this.intercept_ = b;

      return [w, b];
    }
  
    predict(x) {
      return x * this.coef_ + this.intercept_;
    }
  }
  
  // Attach the LR class to the global window object
  window.LR = LR;
  
var primeiroApp = new Vue({
  el: '#primeiroApp',

  data: {
    contador: 'CONTADORRRR',

    timer: null
  }

  // methods: {
  //   toggle: function toggle() {
  //     if (this.timer) {
  //       clearInterval(this.timer);

  //       this.timer = null;
  //     } else {
  //       this.timer = setInterval(function() {
  //         primeiroApp.contador += 1;
  //       }, 1000);
  //     }
  //   },

  //   acaoContador: function acaoContador() {
  //     if (this.timer) {
  //       return 'parar';
  //     } else {
  //       return 'começar';
  //     }
  //   }
  // }
});

var app = new Vue({
  el: '#app',
  delimiters: ['[[[', ']]]'],
  data: {
    message: 'Hello Vue!',
    band: {},
    todos: []
  },
  methods: {
    fetchData: function () {
      this.$http.get('http://127.0.0.1:8020/api/chart').then(response => {
        this.band = response.body;
      }, response => {
        console.log("an error occured");
      });
    }
  },
  mounted: function () {
    this.fetchData();
  }
})

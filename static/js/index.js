// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        query: "",
        results: [],
        add_content: [],
        reply_list: []
    };    
    
    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };    

    app.get_products = function(){
        if (app.vue.query.length > 0){
            axios.get(get_products_url, {params: {q: app.vue.query}})
                .then(function (result) {
                    app.data.results = result.data.results;
                });
        } 
        else {
            app.vue.results = []
        } 
    };

    app.clearQuery = function (){
        app.vue.query = '';
    };

    app.add_post = function () {
        axios.post(add_post_url,
            {
                content: app.vue.add_content,

            }).then(function(response) {
                app.vue.reply_list.push({
                    id: response.data.id,
                    users_id: response.data.users_id,
                    timestamp: response.data.timestamp,
                    timeago : response.data.timeago,
                    content: app.vue.add_content,
                });

            });
            //console.log(app.vue.meow_list);
            app.enumerate(app.vue.reply_list);

    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        get_products: app.get_products,
        clearQuery: app.clearQuery,
        add_post: app.add_post
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it. 
init(app);
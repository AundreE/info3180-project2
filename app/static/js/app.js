/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <a class="navbar-brand" href="#">Photogram Web Application</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
                <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item active">
              <router-link class="nav-link" to="/explore">Explore</router-link>
            </li>
            <li class="nav-item active">
              <router-link class="nav-link" to="#">My Profile</router-link>
            </li>
            <li v-if="token" class="nav-item active">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
            <li v-else class="nav-item">
              <router-link class="nav-link active" to="/login">Login</router-link>
            </li>
        </ul>
      </div>
    </nav>
    `,
     data: function(){
        return {
            token: localStorage.token
        }
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
            <p>Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const Home = Vue.component('home', {
   template: `
    <div class="row landing-container">
        <div class="col-md-4 landing-container-child" style="margin-left: 15%;">
            <img src="/static/images/landing.jpg" id="landing-img"/>
        </div>
        <div class="col-md-4  landing-container-child float-clear">
          <div class="card" style="width: 28rem; height: 23rem; box-shadow: 2px 2px 10px grey;">
            <img class="card-img-top" src="static/images/photogramLogo.png" alt="Card image cap" style="width: 60%; margin: 0 auto; padding-top: 20px;">
            <div class="card-body" style="padding-top: 0px;">
              <hr>
              <p class="card-text">Share photos of your memorable moments with the entire world.</p>
              <div style="margin-top: 20%;">
                  <button class="btn btn-success col-md-5">Register</button>
                  <button class="btn btn-primary col-md-5">Login</button>
              </div>
            </div>
          </div>  
        </div>
    </div>
   `,
    data: function() {
       return {}
    }
});
const Login = Vue.component('login', {
    template:`
      <div>
        <form id="login-form" @submit.prevent="login">
            <div class="card-header center login-header">
              <strong>Login</strong>
            </div>
            <div class="card center">
              <div class="card-body login">
                <div>
                  <label for='usrname'><strong>Username</strong></label><br>
                  <input type='text' id='usrname' name='username' style="width: 100%;"/>
                </div>
                <div>
                  <label for='passwd'><strong>Password</strong></label><br>
                  <input type='password' id='passwd' name='password' style="width: 100%;"/>
                </div>
                <div>
                  <button id="submit" class="btn btn-success">Login</button> 
                </div>
              </div>
            </div>
            <div v-if='messageFlag' >
              <div class="alert alert-danger center" style="width: 20rem; margin-top: 5%;">
                {{ message }}
              </div>
            </div>
        </form>
      </div>
    `,
    methods:{
      login: function(){
        const self = this

        fetch("api/auth/login",{
          method: "POST",
          body: new FormData(document.getElementById('login'))
        }).then(function(response){
          return response.json()
        }).then(function(jsonResponse){
          self.messageFlag = true;

          if(jsonResponse.status == "success"){
            localStorage.token = jsonResponse.message
            router.go();
            router.push("/")
          }else{
            self.message = jsonResponse.message
          }

        }).catch(function(error){
          self.messageFlag = false;
          console.log(error);
        });
      }
    },
    data: function(){
      return {
        messageFlag: false,
        message: ""
      }
    }
});

const register = Vue.component('register',{
  template:`
  <div>
    <h2>Register</h2>
    <div>
    
    <form id="registerform" @submit.prevemt="photoupload" method ='POST' enctype="multipart/form-data">
      <div>
        <div class="fgroup">
          <label>Username</label>
        </div>
        
        <div class="fgroup">
          <label>Password</label>
        </div>
      
        <div class="fgroup">
          <label>First Name</label>
        </div>
        
        <div class="fgroup">
          <label>Last Name</label>
        </div> 
        
        <div class="fgroup">
          <label>Email</label>
        </div>      
        
        <div class="fgroup">
          <label>Location</label>
        </div>      
        
        <div class="fgroup">
          <label>Biography</label>
        </div>      
        
        <div class="btn">
          <label>Photo</label>
          <button id="browbtn">Browse</btn>
          
        </div> 
        
       </div>
       <button class="subbtn" type="submit">Submit</button>
       </form>
    </div>
  </div>
  `,
  data: function() {
    return {
      response: [],
      error: []
    };
  },
  methods: {
    photoupload : function() {
      let self = this;
      let registerform = document.getElementById('registerform');
      let form_data = new FormData(registerform);
      fetch("/api/users/register",{
        method: 'POST',
        body: form_data,
        headers: {
          'X-CSRFToken': token
        },
        credentials: 'same-origin'
      })
      .then(function(jsonResponse){
        return response.json();
      })
      .then(function (jsonResponse){
        console.log(jsonResponse);
      })
      .catch(function(error){
        console.log(error);
      });
    }
  }
    
})

// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/", component: Home },
        { path: "/register", component: Register},
        { path: "/login",},
        {path: "/logout",},
        {path: "explore"},
        
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});
/* Add your Application JavaScript */
//FIX HEADER & FOOTER COMPONENTS
Vue.component('app-header', {
    template: `
   
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top" style="background-color:#4c8ef7;">
      <a class="navbar-brand" href="#"><img src='http://www.yim778.com/data/out/217/1289093.png' class='image1' alt='camera' style="width:35px; height:35px;"><h4>Photogram</h4></i></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        
          <li class="nav-item active">
            <router-link class="nav-link"to="/">Home <span class="sr-only">(current)</span></router-link>
          </li>
          
          <!--<li class="nav-item active">
            <router-link class="nav-link" to="/register">Register<span class="sr-only">(current)</span></router-link>
          </li>-->
          
          <li class="nav-item active">
            <router-link class="nav-link" to="/explore">Explore<span class="sr-only">(current)</span></router-link>
          </li>
          
          <li class="nav-item active">
            <router-link class="nav-link" :to="{ name: 'profile', params: { user_id: userid }}">My Profile<span class="sr-only">(current)</span></router-link>
          </li>
          
          
          
          <li class="nav-item active">
            <router-link class="nav-link" to="/logout">Logout <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>
      </div>
    </nav>
    `,
    beforeCreate: function() {
        let self = this;
        
        bus.$on('updateId', function(user_id) {
            self.userid = user_id;
            console.log(user_id);
        })
    },
    data: function() {
        return {
            userid: ''
        }
    }
});

var bus = new Vue()

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
            <p>Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const Register = Vue.component('register', {
    template: `
    <html>
        <div class="jumbotron">
            <h2>Register</h2>
            <div id='conta'>
                <div v-if="messages.errors" v-for="m in messages" class="alert alert-danger">
                    <li v-for="error in m">    
                        {{ error }}
                    </li>
                </div>
                <div v-else="messages.info" v-for="info in messages" class="alert alert-success">
                    {{ info.message }}
                </div>
                
                <form method="post" enctype="multipart/form-data" id="registerForm" @submit.prevent="uploadInfo">
                    <br>
                    <label> Username </label><br>
                    <input type="text" name="username"><br>
                    <br>
                    
                    <label> Password </label><br>
                    <input type="password" name="password"><br>
                    <br>
            
                    <label> First Name </label><br>
                    <input type="text" name="firstname"><br>
                    <br>
                    
                    <label> Last Name </label><br>
                    <input type="text" name="lastname"><br>
                    <br>
            
                    <label> Email </label><br>
                    <input type="text" name="email"><br>
                    <br>
            
                    <label> Location </label><br>
                    <input type="text" name="location"><br>
                    <br>
            
                    <label> Biography </label><br>
                    <textarea name="biography"></textarea><br>
                    <br>
                    
                    <div>
                        <label for="photo">Photo</label>
                        <div> <input type="file" id="photo" name="profile_photo" /> </div>
                    </div>
                    <br><br>
                    
                    <button class="btn btn-success2" type="submit" name="submit">Register</button>
                </form>
            </div>
        </div>
    </html>
    `,
    methods: {
        uploadInfo: function() {
            let registerForm = document.getElementById('registerForm');
            let form_data = new FormData(registerForm);
            let self = this;
            
            fetch("/api/users/register", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                    console.log(jsonResponse);
                    
                    if (jsonResponse.hasOwnProperty('info'))
                    {
                        console.log(jsonResponse.info);
                        router.push('/login');
                    }
                    else if (jsonResponse.hasOwnProperty('errors'))
                    {
                        console.log(jsonResponse.errors);
                    }
                    self.messages = jsonResponse;
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
        
    },
    data: function() {
        return {
            messages: []
        }
    }
});

const Login = Vue.component('login', {
    template: `
    <html>
        <div class="jumbotron">
            <h2>Login</h2>
            <div id='contain'>
                <div v-if="messages.errors" v-for="m in messages" class="alert alert-danger">
                    <li v-for="error in m">    
                        {{ error }}
                    </li>
                </div>
                <div v-else="messages.info" v-for="info in messages" class="alert alert-success">
                    {{ info.message }}
                </div>
                
                <form method="POST" enctype="multipart/form-data" id="loginForm" @submit.prevent="authUser">
                <br>
                    <label> Username </label><br>
                    <input type="text" name="username"><br>
                    <br>
                
                    <label> Password </label><br>
                    <input type="password" name="password"><br>
                    <br>
        
                    <button class="btn btn-success3" type="submit" name="submit">Login</button>
                </form>
            </div>
        </div>
    </html>
    `,
    methods: {
        authUser: function() {
            let loginForm = document.getElementById('loginForm');
            let form_data = new FormData(loginForm);
            let self = this;
            
            fetch("/api/auth/login", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                    console.log(jsonResponse);
                    
                    if (jsonResponse.hasOwnProperty('info'))
                    {
                        let jwt_token = jsonResponse.info.token;
                        let decoded_token = parseJwt(jwt_token);
                        let user_id = decoded_token.user_id;
                        console.log(user_id);
                        
                        localStorage.setItem('token', jwt_token);
                        localStorage.setItem('user_id', user_id);
                        bus.$emit('updateId', user_id);
                    
                        console.info('Token generated and added to localStorage.');
                        self.token = jwt_token;
                        router.push('/explore');
                    }
                    else if (jsonResponse.hasOwnProperty('errors'))
                    {
                        console.log(jsonResponse.errors);
                    }
                    self.messages = jsonResponse;
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    data: function() {
        return {
            messages: [],
            token: ''
        }
    }
});

function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace('-', '+').replace('_', '/');
    return JSON.parse(window.atob(base64));
}
        
const Logout = Vue.component('logout', {
    template: `
    `,
    created: function() {
        fetch("/api/auth/logout", {
            method: 'GET',
            'headers': {
                // JWT requires the Authorization schema to be `Bearer` instead of `Basic`
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                console.log(jsonResponse);
                    
                if (jsonResponse.hasOwnProperty('info'))
                {
                    localStorage.removeItem('token');
                    console.info('Token removed from localStorage.');
                    
                    localStorage.removeItem('user_id');
                    console.info('User ID removed from localStorage.');
                        
                    self.messages = jsonResponse;
                    router.push('/');
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    data: function() {
        return {
            messages: []
        }
    }
});

const Explore = Vue.component('explore', {
    template: `
    <html>
    <div class='jumbotron'>
       <br><br>
       <button class="btn btn-primary" id="exBtn" @click="makePost">New Post</button>
       <div id="container1">
          <div v-for="post in posts">
                <div class="card">
                    <div class="card-header">
                        <img :src="'/static/images/icon.png'" id="iconImg"/> 
                        <a @click="viewUser(post.user_id)"> {{ post.username }} </a>
                    </div>
                    
                    <!--<div class="card-body">
                        <img :src="'/static/uploads/' + post.photo" id="postImg" />
                    </div>-->
                    
        
                    <!--<div id='postImg'>
                        <img :src="'/static/uploads/' + post.photo" id="postImg" class="postImg" alt="Girl in a jacket" style="width:1000px;height:1000px;">
                    </div>-->
                    
                    <div class="info2">
                        <div id='postImg'>
                        <img :src="'/static/uploads/' + post.photo" id="postImg" class="postImg" alt="Girl in a jacket" style="width:1000px;height:1000px;">
                        </div>
                    </div>
                    <br>
                    <br>
                    <div class="info"><br>
                            {{ post.caption }}<br><br><br><br>
                            <img :src="'/static/images/instagram-heart-icon-vector-10.jpg'" v-if="liked === 'false'" id="iconImg" @click="likePost(post.id)" />
                            <img :src="'/static/images/Instagram-Heart-Free-Download-PNG.png'" v-if="liked === 'true'" id="iconImg" />
                            <div id="numlikes"> {{ post.likes }} Likes </div>
                            <div id="postdate"> {{ post.created_on }} </div>
                        </div>
                    
                    <!--<div class="card-footer">
                        <div id="numlikes" v-show="liked == false">{{ post.likes }} </div>
                        <div id="numlikes" v-show="liked == true">{{ likes }}</div>
                        <div id="postdate"> {{ post.created_on }} </div>
                    </div>-->
                </div><br>
                <br></br>
                <p>      </p>
            </div><br>
            <br>
       </div>
       </div>
    </html>
    `,
    created: function() {
        let self = this;
        self.liked = 'false';
        
        fetch("/api/posts", {
            method: 'GET',
            'headers': {
                // JWT requires the Authorization schema to be `Bearer` instead of `Basic`
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                console.log(jsonResponse);
                    
                if (jsonResponse.hasOwnProperty('info'))
                {
                    self.posts = jsonResponse.info.posts;
                    console.log(jsonResponse.info);
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    methods: {
        makePost: function() {
            let self = this;
            
            self.$router.push({path: '/posts/new'});
        },
        viewUser: function(next_id) {
            localStorage.setItem('next_id', next_id);
            router.push({
                name: 'profile',
                params: {
                    user_id: next_id
                }
            });
        },
        likePost: function(post_id) {
            let self = this;
        
            fetch("/api/posts/"+ post_id +"/like", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token,
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                    console.log(jsonResponse);
                        
                    if (jsonResponse.hasOwnProperty('info'))
                    {
                        if (jsonResponse.info.message)
                        {
                            console.log(jsonResponse.info.message);
                            let likes = jsonResponse.info.likes;
                            self.liked = 'true';
                            let index = 0;
                            for (i = 0; i < self.posts.length; i++) {
                                if (self.posts[i].id == post_id) {
                                    index = i;
                                    break;
                                }
                            }
                            self.posts[index].likes = likes;
                        }
                        else if (jsonResponse.info.error)
                        {
                            console.log(jsonResponse.info.error);
                        }
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    data: function() {
        return {
            posts: [],
            message: '',
            likes: '',
            liked: ''
        }
    }
});

const Profile = Vue.component('profile', {
    template: `
    <html>
    <div class="jumbotron">
        <div class="card" id='cardy'>
            <div class="card-body">
                <img :src="'/static/uploads/' + user.profile_photo" id="profileImg"/>
                
                <div class="info">
                    <h4 class="card-title">{{ user.first_name }} {{ user.last_name }}</h4>
                    <div> {{ user.location }} </div>
                    
                    <div> Member since {{ user.joined_on }} </div>
                    <br>
                    <br>
                    <div> {{ user.bio }} </div>
                </div>
                <button class="btn btn-primary" id="follow-btn" v-cloak @click="followUser(user.id)">Follow</button>
            </div>
        </div>
        <div> {{ followers }} Followers </div>
        <div class='container'>
         <div v-for="post in posts">
            <img :src="'/static/uploads/' + post.photo" class="grid-item"/>
         </div>
         </div>
    </div>
    </html>
    `,
    beforeCreate: function() {
        let self = this;
        self.user = {};
        self.posts = [];
        self.followers = 0;
        let user_id = this.$route.params.user_id;
       
        fetch("/api/users/" + user_id + "/follow", {
            method: 'POST',
            headers: {
                'X-CSRFToken': token,
                Authorization: 'Bearer ' + localStorage.getItem('token')
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                console.log(jsonResponse);
                    
                if (jsonResponse.hasOwnProperty('info'))
                {
                    console.log(jsonResponse.info);
                    
                    let followBtn = document.getElementById('follow-btn');
                    
                    if (jsonResponse.info.message)
                    {
                        followBtn.innerHTML="Follow";
                    } else if (jsonResponse.info.error)
                    {
                        followBtn.innerHTML="Following";
                    }
                    
                    if (user_id == localStorage.user_id)
                    {
                        followBtn.style.display = 'none';
                    }
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    created: function() {
        let self = this;
        let user_id = this.$route.params.user_id;
        self.followers = 0;
        console.log('profile (passed)', user_id);
        console.log('profile', localStorage.user_id);
        
        fetch("/api/users/"+ user_id, {
            method: 'GET',
            'headers': {
                // JWT requires the Authorization schema to be `Bearer` instead of `Basic`
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
                console.log(jsonResponse);
                    
                if (jsonResponse.hasOwnProperty('info'))
                {
                    self.user = jsonResponse.info.user;
                    self.posts = jsonResponse.info.posts;
                    console.log(jsonResponse.info);
                    self.followers = getFollowers(user_id);
                }
                
                self.message = jsonResponse.info;
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    methods: {
       followUser: function(user_id) {
           let self = this;
        //   let user_id = this.$route.params.user_id;
           
           fetch("/api/users/" + user_id + "/follow", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token,
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                    console.log(jsonResponse);
                        
                    if (jsonResponse.hasOwnProperty('info'))
                    {
                        console.log(jsonResponse.info);
                        
                        if (jsonResponse.info.message)
                        {
                            let followBtn = document.getElementById('follow-btn');
                            
                            followBtn.innerHTML="Following";
                            followBtn.setAttribute("class", "btn btn-success");
                            
                            self.followers = getFollowers(user_id);
                        }
                        else if (jsonResponse.info.error)
                        {
                            console.log(jsonResponse.info.error);
                        }
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    },
    data: function() {
        return {
            posts: [],
            message: '',
            followers: '',
            id: ''
        }
    }
});

function getFollowers(user_id) {
    let self = this;
    
    fetch("/api/users/" + user_id + "/follow", {
        method: 'GET',
            headers: {
            'X-CSRFToken': token,
            Authorization: 'Bearer ' + localStorage.getItem('token')
        },
        credentials: 'same-origin'
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            console.log('Followers: ',jsonResponse.info.followers);
                
            return jsonResponse.info.followers;
        })
        .catch(function (error) {
            console.log(error);
        });
}

const NewPost = Vue.component('newPost', {
    template: `
    <html>
        <div class='jumbotron'>
            <div id="justneedaroot">
                <br>
                <h2>New Post</h2>
                <div id='contain'>
                    <br>
                    <br>
                    <div v-if="messages.errors" v-for="m in messages" class="alert alert-danger">
                        <li v-for="error in m">    
                            {{ error }}
                        </li>
                    </div>
                    <div v-else="messages.info" v-for="info in messages" class="alert alert-success">
                        {{ info.message }}
                    </div>
                    
                    <form method="POST" enctype="multipart/form-data" id="postForm" @submit.prevent="createPost">
                        <h5><label for="photo">Photo</label></h5>
                        <input type="file" id="photo" name="photo" />
                        
                        <br><br><h5><label for="caption"> Caption </label></h5>
                        <textarea id="caption" name="caption" placeholder="Write a caption"></textarea><br><br>
                        <button class="btn btn-success" id='buttn' type="submit" name="submit">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </html>
    `,
    methods: {
        createPost: function() {
            let postForm = document.getElementById('postForm');
            let form_data = new FormData(postForm);
            let self = this;
            let user_id = localStorage.user_id;
            
            fetch("/api/users/" + user_id + "/posts", {
                method: 'POST',
                body: form_data,
                headers: {
                    'X-CSRFToken': token,
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                    console.log(jsonResponse);
                        
                    if (jsonResponse.hasOwnProperty('info'))
                    {
                        console.log(jsonResponse.info);
                    }
                    else if (jsonResponse.hasOwnProperty('errors'))
                    {
                        console.log(jsonResponse.errors);
                    }
                    self.messages = jsonResponse;
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
        
    },
    data: function() {
        return {
            messages: []
        }
    }
});



const Home = Vue.component('home', {
   template: `
   <html>
        <div class="jumbotron">
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <div id='pic'>
        <img src="https://graffica.info/wp-content/uploads/2015/02/Paisaje-de-agua-77223.jpg" class="image2" alt="Girl in a jacket" style="width:1000px;height:850px;">
        </div>
        <div id='cont'>
            <i class="material-icons" style="font-size:45px">camera_alt</i><h1>Photogram</h1>
            <hr>
            <p class="lead">Photogram allows family members and friends to share pictures with each other.</p>
            <br>
            <br>
            <div class='but'>
            <div id='left'>
            <button class="btn btn-success"@click="gotoregister" >Register</button>
            </div>
            <div id='right'>
            <button class="btn btn-primary" @click="gotologin">Login</button>
            </div>
            </div>
        </div>
        </div>
    </html>
   `,
    data: function() {
       return {}
    },
    methods:
    {
        gotologin: function()
        {
            let self=this;
            //const self=this;
            self.$router.push({path: '/login'})
        },
        gotoregister: function()
        {
            //t.self=this;
            const self=this
            self.$router.push({path: '/register'})
        }
        
    }
});

// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/", component: Home },
        { path: "/register", component: Register },
        { path: "/login", component: Login },
        { path: "/logout", component: Logout },
        { path: "/explore", component: Explore },
        { path: "/users/:user_id", name: 'profile', component: Profile },
        { path: "/posts/new", component: NewPost }
    ]
});

router.afterEach(function (transition) {
  console.log('current' + transition.path);
});

// Instantiate our main Vue Instance
const app = new Vue({
    el: "#app",
    router
});
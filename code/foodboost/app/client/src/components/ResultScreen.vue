<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 100vh;">
    <div class="card" style="width: 70vh; height: 90vh; border: 0">
      <div class="card-header text-white text-center p-3" style="background: #303443">
        <h2>ADS - Groep 6</h2>
      </div>
      <div class="card-body p-3 d-flex justify-content-center" style="background: #acadaf">
        <div class="card card-style mb-2" style="width: 90%">
          <div v-if="recommended_recipes && error === false">
            <div class="text-center">
              <h4 class="p-1">Resultaat</h4>
            </div>
            <div class="p-3">
              <h6>Wij raden u vandaag de {{ kitchen }}e keuken aan:</h6>
              <div class="p-2">
                <div class="row">
                  <div class="col-md-6">
                    <div class="card">
                      <a :href="this.recommended_recipes[0].url" target="_blank">
                        <img :src="this.recommended_recipes[0].image" alt="recipe" class="card-img-top">
                      </a>
                      <div class="card-body p-2">
                        <p class="card-text">{{this.recommended_recipes[0].name}}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6 mb-5">
                    <div class="card">
                      <a :href="this.recommended_recipes[1].url" target="_blank">
                        <img :src="this.recommended_recipes[1].image" alt="recipe" class="card-img-top">
                      </a>
                      <div class="card-body p-2">
                        <p class="card-text">{{this.recommended_recipes[1].name}}</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="card">
                      <a :href="this.recommended_recipes[2].url" target="_blank">
                        <img :src="this.recommended_recipes[2].image" alt="recipe" class="card-img-top">
                      </a>
                      <div class="card-body p-2">
                        <p class="card-text">{{this.recommended_recipes[2].name}}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card">
                      <a :href="this.recommended_recipes[3].url" target="_blank">
                        <img :src="this.recommended_recipes[3].image" alt="recipe" class="card-img-top">
                      </a>
                      <div class="card-body p-2">
                        <p class="card-text">{{this.recommended_recipes[3].name}}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="recommended_recipes == null && error === false">
            <div class="text-center">
              <h4 class="p-2">Laden..</h4>
            </div>
          </div>
          <div v-if="error === true">
            <div class="text-center">
              <h4 class="p-2">Er ging iets mis. Probeer het opnieuw</h4>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer" style="background: #303443">
        <div class="row justify-content-center p-3">
          <button type="button" class="btn btn-primary" @click="goBackToHome()">
              Terug naar het begin
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userId: 0,
      kitchen: null,
      recommended_recipes: null,
      error: false
    };
  },
  props: ['likedRecipes'],
  methods: {
    postUserData() {
      const path = 'http://localhost:5000/post_get_user_result';
      axios.post(path, { likedRecipes: this.likedRecipes} )
        .then((res) => {
          if (res.data.status === "success") {
            console.log("Response:", res);

            this.kitchen = res.data.data.kitchen
            this.recommended_recipes = res.data.data.recipes;
            console.log(this.recommended_recipes)
          }
          else {
            console.log("Error:", res);
            this.error = true;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    goBackToHome() {
      this.$router.push({ name: 'SwipeScreen' });
    }
  },
  created() {
    this.postUserData();
  },
}
</script>

<style scoped>

</style>

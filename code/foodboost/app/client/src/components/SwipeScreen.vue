<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 100vh;">
    <div class="card" style="width: 70vh; height: 90vh; border: 0">
      <div class="card-header text-white text-center p-3" style="background: #303443">
        <h2>ADS - Groep 6</h2>
        <br>
        <h4>Like nog <span style="color: green; font-size: xx-large">{{ counter }}</span> recepten voor het resultaat</h4>
      </div>
      <div class="card-body p-5 d-flex justify-content-center" style="background: #acadaf">
        <recipe :recipe="recipe"></recipe>
      </div>
      <div class="card-footer" style="background: #303443">
        <div class="row justify-content-center p-3">
          <div class="col-1 ml-5 mr-5">
            <button type="button" class="btn btn-danger btn-circle btn-xl"
              @click="dislikeRecipe()">
            </button>
          </div>
          <div class="col-1 ml-5 mr-5">
            <button type="button" class="btn btn-success btn-circle btn-xl"
              @click="likeRecipe()">
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Recipe from './Recipe.vue';

export default {
  data() {
    return {
      recipes: [],
      likedRecipes: [],
      recipe: {},
      userId: 0,
      counter: 10,
    };
  },
  props: ['preferences'],
  components: {
    recipe: Recipe,
  },
  methods: {
    getRecipes() {
      const path = 'http://localhost:5000/get_recipes';
      axios.post(path, { preferences: this.preferences} )
        .then((res) => {
          this.recipes = JSON.parse(res.data.recipes);
          this.recipe = this.recipes[Math.floor(Math.random() * this.recipes.length)];
        })
        .catch((error) => {
          console.error(error);
        });
    },
    likeRecipe() {
      this.likedRecipes.push(this.recipe.index);
      console.log(this.likedRecipes)

      if (this.counter === 1) {
        this.$router.push({ name: 'ResultScreen', params: { likedRecipes: JSON.stringify(this.likedRecipes) } });
      }
      else {
        this.counter -= 1
        this.recipe = this.recipes[Math.floor(Math.random() * this.recipes.length)];
      }
    },
    dislikeRecipe() {
      this.recipe = this.recipes[Math.floor(Math.random() * this.recipes.length)];
    },
  },
  created() {
    this.getRecipes();
  },
};
</script>

<style type="text/css">

.btn-circle.btn-xl {
  width: 70px;
  height: 70px;
  padding: 10px 16px;
  border-radius: 35px;
  font-size: 12px;
  text-align: center;
}
</style>

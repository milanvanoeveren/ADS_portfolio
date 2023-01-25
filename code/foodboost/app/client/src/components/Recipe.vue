<template>
  <div class="card card-style" style="width: 90%">
    <a :href="recipe.url" target="_blank" style="height: 60%">
      <img width="100%" height="100%" :src="recipe.image" alt="Foto">
    </a>
    <div class="text-center">
      <h4 class="p-2">{{ recipe.name }}</h4>
      <div class="row justify-content-start p-3 mb-5">
        <div class="col text-left font-weight-bold">
          <p>Personen:</p>
          <p>Tijd:</p>
          <p>Calorieën:</p>
        </div>
        <div class="col text-left">
          <p>{{ recipe.persons }}</p>
          <p>{{ recipe.time }} min</p>
          <p>{{ recipe.calories }} kcal</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: ['recipe'],
};
</script>

<style type="text/css">

.card-style {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  width: 40%;
}
</style>

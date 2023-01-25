<template>
  <div class="d-flex justify-content-center align-items-center" style="min-height: 100vh;">
    <div class="card" style="width: 70vh; height: 90vh; border: 0">
      <div class="card-header text-white text-center p-3" style="background: #303443">
        <h2>ADS - Groep 6</h2>
      </div>
      <div class="card-body p-5 d-flex justify-content-center" style="background: #acadaf">
        <div class="card card-style" style="width: 90%">
          <div class="text-center p-3">
            <h3>Selecteer je voorkeuren</h3>
          </div>
          <div class="ml-3">
            <div class="form-check mb-2">
              <input class="form-check-input" type="checkbox" value="glutenvrij" id="glutenvrij">
              <label class="form-check-label" for="glutenvrij">
                Glutenvrij
              </label>
            </div>
            <div class="form-check mb-2">
              <input class="form-check-input" type="checkbox" value="vegetarisch" id="vegetarisch">
              <label class="form-check-label" for="vegetarisch">
                Vegetarisch
              </label>
            </div>
            <div class="form-check mb-2">
              <input class="form-check-input" type="checkbox" value="lactosevrij" id="lactosevrij">
              <label class="form-check-label" for="lactosevrij">
                Lactosevrij
              </label>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer text-center" style="background: #303443">
        <button class="btn btn-primary" @click="nextScreen()">Ga door</button>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      preferences: [],
    };
  },
  methods: {
    nextScreen() {
      const inputs = document.getElementsByTagName('input');
      for (let i = 0; i < 3; i++) {
        if (inputs[i].checked) {
          this.preferences.push(inputs[i].id)
        }
      }
      this.$router.push({ name: 'SwipeScreen', params: { preferences: JSON.stringify(this.preferences) } });
    },
  },
};
</script>

<style scoped>

</style>

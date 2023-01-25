import Vue from 'vue';
import Router from 'vue-router';
import Questions from '../components/Questions.vue';
import SwipeScreen from '../components/SwipeScreen.vue';
import ResultScreen from "../components/ResultScreen";

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/Questions',
      name: 'Questions',
      component: Questions,
      props: true,
    },
    {
      path: '/',
      name: 'SwipeScreen',
      component: SwipeScreen,
      props: true,
    },
    {
      path: '/ResultScreen',
      name: 'ResultScreen',
      component: ResultScreen,
      props: true,
    },
  ],
});

// Vue Router configuration

import Vue from "vue";
import VueRouter from "vue-router";
import store from "./store";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      redirect: { name: "public" }
    },
    {
      name: "public",
      path: "/public",
      meta: { layout: "arco" },
      component: () => import("@/pages/Public")
    },
    {
      name: "login",
      path: "/login",
      meta: { layout: "arco" },
      component: () => import("@/pages/Login")
    },
    {
      name: "admin",
      path: "/admin",
      meta: { authRequired: true },
      component: () => import("@/pages/Admin")
    },
    {
      name: "people",
      path: "/people",
      meta: { authRequired: true },
      component: () => import("@/pages/People")
    },
    {
      name: "groups",
      path: "/groups",
      meta: { authRequired: true },
      component: () => import("@/pages/Groups")
    },
    {
      name: "events",
      path: "/events",
      meta: { authRequired: true },
      component: () => import("@/pages/Events"),
      redirect: { name: "all" },
      children: [
        {
          name: "all",
          path: "all",
          meta: { authRequired: true },
          component: () => import("@/components/events/EventTable")
        },
        {
          name: "event",
          path: ":event",
          meta: { authRequired: true },
          redirect: { name: "details" },
          component: () => import("@/components/events/Event"),
          children: [
            {
              name: "details",
              path: "details",
              meta: { authRequired: true },
              component: () => import("@/components/events/EventDetails")
            },
            {
              name: "participants",
              path: "participants",
              meta: { authRequired: true },
              component: () => import("@/components/events/EventParticipants")
            },
            {
              name: "teams",
              path: "teams",
              meta: { authRequired: true },
              component: () => import("@/components/events/teams/EventTeams")
            },
            {
              name: "assets",
              path: "assets",
              meta: { authRequired: true },
              component: () => import("@/components/events/assets/EventAssets")
            }
          ]
        }
      ]
    },
    {
      name: "locale",
      path: "/locale",
      meta: { authRequired: true },
      component: () => import("@/pages/Locale")
    },
    {
      name: "diplomas-admin",
      path: "/diplomas",
      meta: { authRequired: true },
      component: () => import("@/pages/Diplomas")
    },
    {
      name: "courses-admin",
      path: "/courses",
      meta: { authRequired: true },
      component: () => import("@/pages/Courses")
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.authRequired)) {
    // The destination requires authentication.
    if (store.getters.isLoggedIn) {
      // But we're already logged in.
      next();
    } else {
      // So redirect to the login page; retain
      // the desired page for a later redirect.
      next({
        name: "login",
        query: { redirect: to.name }
      });
    }
  } else {
    // The destination doesn't require authentication.
    next();
  }
});

export default router;

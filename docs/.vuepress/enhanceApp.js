/**
 * Client app enhancement file.
 *
 * https://v1.vuepress.vuejs.org/guide/basic-config.html#app-level-enhancements
 */

import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

export default ({
  Vue, // the version of Vue being used in the VuePress app
  options, // the options for the root Vue instance
  router, // the router instance for the app
  siteData // site metadata
}) => {
  Vue.use(Vuetify);
  options.vuetify = new Vuetify({
    icons: {
      iconfont: "fa",
      values: {
        //
      }
    }
  });

  if (typeof process === "undefined" || process.env.VUE_ENV !== "server") {
    router.onReady(() => {
      const { app } = router;
      app.$once("hook:mounted", () => {
        // temporary fix for https://github.com/vuejs/vuepress/issues/2428
        setTimeout(() => {
          const { hash } = document.location;
          if (hash.length > 1) {
            const id = decodeURI(hash.substring(1));
            const element = document.getElementById(id);
            if (element) element.scrollIntoView();
          }
        }, 500);
      });
    });
  }
};

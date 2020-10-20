<template>
  <v-app>
    <v-main>
      <v-card>
        <v-card-title>...</v-card-title>
      </v-card>
    </v-main>
  </v-app>
</template>

<script>
import plugins from "../public/plugins.json";

export default {
  name: "Plugins",
  data() {
    return {
      plugins: plugins
    };
  }
};
</script>

<style>
.v-application--wrap {
  min-height: 0 !important;
}
</style>

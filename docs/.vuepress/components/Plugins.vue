<template>
  <v-app>
    <v-main>
      <v-row>
        <v-col
          cols="12"
          sm="6"
          md="4"
          v-for="(plugin, index) in plugins"
          :key="index"
        >
          <v-card>
            <v-card-title>{{ plugin.name }}</v-card-title>
            <v-card-text>{{ plugin.desc }}</v-card-text>
          </v-card>
        </v-col>
      </v-row>
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

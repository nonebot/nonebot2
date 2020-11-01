<template>
  <div class="plugins">
    <!-- TODO: Search and New -->
    <hr />
    <v-app>
      <v-main>
        <v-row>
          <v-col
            cols="12"
            sm="6"
            v-for="(plugin, index) in plugins"
            :key="index"
          >
            <v-card>
              <v-card-title>
                {{ plugin.name }}
                <v-spacer></v-spacer>
                <a
                  class="repo-link"
                  v-if="repoLink(plugin.repo)"
                  rel="noopener noreferrer"
                  target="_blank"
                  :title="plugin.repo"
                  :href="repoLink(plugin.repo)"
                >
                  <v-icon>fab fa-github</v-icon>
                </a>
              </v-card-title>
              <v-card-text>{{ plugin.desc }}</v-card-text>
              <v-card-actions>
                <v-btn
                  block
                  depressed
                  class="btn-copy"
                  @click="copyCommand(plugin)"
                >
                  copy nb-cli command
                  <v-icon right small>fa-copy</v-icon>
                </v-btn>
                <v-snackbar v-model="snackbar">Copied!</v-snackbar>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import copy from "copy-to-clipboard";
import plugins from "../public/plugins.json";

export default {
  name: "Plugins",
  data() {
    return {
      plugins: plugins,
      snackbar: false
    };
  },
  methods: {
    repoLink(repo) {
      if (repo) {
        return /^https?:/.test(repo) ? repo : `https://github.com/${repo}`;
      }
      return null;
    },
    copyCommand(plugin) {
      copy(`nb plugin install ${plugin.id}`, {
        format: "text/plain"
      });
      this.snackbar = true;
    }
  }
};
</script>

<style>
.v-application--wrap {
  min-height: 0 !important;
}
</style>

<style scoped>
.repo-link {
  text-decoration: none !important;
  display: inline-block;
}
.repo-link:hover i {
  color: #ea5252;
}
</style>

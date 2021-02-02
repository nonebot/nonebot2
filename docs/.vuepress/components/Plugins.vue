<template>
  <div class="plugins">
    <v-app>
      <v-main>
        <v-row>
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="filterText"
              dense
              rounded
              outlined
              clearable
              hide-details
              label="Filter Plugin"
            >
              <template v-slot:prepend-inner>
                <div class="v-input__icon v-input__icon--prepend-inner">
                  <v-icon small>fa-filter</v-icon>
                </div>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn
              block
              color="primary"
              target="_blank"
              rel="noopener noreferrer"
              href="https://github.com/nonebot/nonebot2/issues/new?labels=Plugin&template=plugin-publish.md&title=Plugin%3A+blabla+的插件"
              >Publish Your Plugin
            </v-btn>
          </v-col>
          <v-col cols="12" sm="4">
            <v-pagination
              v-model="page"
              :length="pageNum"
              prev-icon="fa-caret-left"
              next-icon="fa-caret-right"
            ></v-pagination>
          </v-col>
        </v-row>
        <hr />
        <v-row>
          <v-col
            cols="12"
            sm="6"
            v-for="(plugin, index) in displayPlugins"
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
              <v-card-text>
                <v-icon x-small>fa-fingerprint</v-icon>
                {{ plugin.id }}
                <v-icon x-small class="ml-2">fa-user</v-icon>
                {{ plugin.author }}
              </v-card-text>
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
        <v-row>
          <v-col cols="12">
            <v-pagination
              v-model="page"
              :length="pageNum"
              prev-icon="fa-caret-left"
              next-icon="fa-caret-right"
            ></v-pagination>
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
      snackbar: false,
      filterText: "",
      page: 1
    };
  },
  computed: {
    pageNum() {
      return Math.ceil(this.filteredPlugins.length / 10);
    },
    filteredPlugins() {
      return this.plugins.filter(plugin => {
        return (
          plugin.id.indexOf(this.filterText) != -1 ||
          plugin.name.indexOf(this.filterText) != -1 ||
          plugin.desc.indexOf(this.filterText) != -1 ||
          plugin.author.indexOf(this.filterText) != -1
        );
      });
    },
    displayPlugins() {
      return this.filteredPlugins.slice((this.page - 1) * 10, this.page * 10);
    }
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

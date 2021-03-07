<template>
  <v-card flat class="plugins">
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
        <v-dialog v-model="dialog" max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn dark block color="primary" v-bind="attrs" v-on="on"
              >Publish Your Plugin
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">Plugin Information</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="newPluginForm" v-model="valid" lazy-validation>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newPlugin.name"
                        label="插件名称"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newPlugin.desc"
                        label="插件介绍"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newPlugin.link"
                        label="PyPI 项目名"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newPlugin.id"
                        label="插件 import 包名"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="newPlugin.repo"
                        label="仓库/主页链接"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialog = false">
                Close
              </v-btn>
              <v-btn
                :disabled="!valid"
                color="blue darken-1"
                text
                @click="
                  dialog = false;
                  publishPlugin();
                "
              >
                Publish
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
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
        <PublishCard
          :name="plugin.name"
          :desc="plugin.desc"
          :id="plugin.id"
          :author="plugin.author"
          :link="plugin.repo"
          text="copy nb install command"
          :command="`nb plugin install ${plugin.id}`"
        ></PublishCard>
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
  </v-card>
</template>

<script>
import PublishCard from "./PublishCard.vue";
import plugins from "../public/plugins.json";

export default {
  name: "Plugins",
  components: {
    PublishCard
  },
  data() {
    return {
      plugins: plugins,
      filterText: "",
      page: 1,
      dialog: false,
      valid: false,
      newPlugin: {
        name: null,
        desc: null,
        id: null,
        link: null,
        repo: null
      }
    };
  },
  computed: {
    pageNum() {
      return Math.ceil(this.filteredPlugins.length / 10);
    },
    filteredPlugins() {
      return this.plugins.filter(plugin => {
        return (
          plugin.id.indexOf(this.filterText || "") != -1 ||
          plugin.name.indexOf(this.filterText || "") != -1 ||
          plugin.desc.indexOf(this.filterText || "") != -1 ||
          plugin.author.indexOf(this.filterText || "") != -1
        );
      });
    },
    displayPlugins() {
      return this.filteredPlugins.slice((this.page - 1) * 10, this.page * 10);
    },
    publishPlugin() {
      if (!this.$refs.newPluginForm.validate()) {
        return;
      }
      const title = encodeURIComponent(
        `Plugin: ${this.newPlugin.name}`
      ).replace(/%2B/gi, "+");
      const body = encodeURIComponent(
        `
**插件名称：**

${this.newPlugin.name}

**插件功能：**

${this.newPlugin.desc}

**PyPI 项目名：**

${this.newPlugin.link}

**插件 import 包名：**

${this.newPlugin.id}

**插件项目仓库/主页链接：**

${this.newPlugin.repo}

<!-- DO NOT EDIT ! -->
<!--
- id: ${this.newPlugin.id}
- link: ${this.newPlugin.link}
- name: ${this.newPlugin.name}
- desc: ${this.newPlugin.desc}
- repo: ${this.newPlugin.repo}
-->
`.trim()
      ).replace(/%2B/gi, "+");
      window.open(
        `https://github.com/nonebot/nonebot2/issues/new?title=${title}&body=${body}&labels=Plugin`
      );
    }
  }
};
</script>

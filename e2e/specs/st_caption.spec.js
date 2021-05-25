/**
 * @license
 * Copyright 2018-2021 Streamlit Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

describe("st.caption", () => {
  before(() => {
    cy.visit("http://localhost:3000/");
  });

  it("displays correct number of elements", () => {
    cy.get(".element-container .stMarkdown small").should("have.length", 5);
  });

  it("matches snapshot", () => {
    cy.get(".element-container .stMarkdown small").then(els => {
      cy.wrap(els.slice(1)).each((el, i) => {
        return cy.wrap(el).matchImageSnapshot(`caption-${i}`);
      });
    });
  });

  it("displays correct content inside caption", () => {
    cy.get(".element-container .stMarkdown small").then(els => {
      expect(els[1].textContent).to.eq("This is a caption!");
      expect(els[2].textContent).to.eq(
        "This is a caption that contains markdown inside it!"
      );
      cy.wrap(els[2])
        .get("em")
        .should("have.text", "caption");
      cy.wrap(els[2])
        .get("strong")
        .should("have.text", "markdown inside it");
      // html should be escaped
      expect(els[3].textContent).to.eq(
        "This is a caption that contains <div>html</div> inside it!"
      );
    });
  });

  it("matches snapshot in sidebar", () => {
    cy.get("[data-testid='stSidebar'] .stMarkdown").matchImageSnapshot(
      `caption-in-sidebar`
    );
  });
});

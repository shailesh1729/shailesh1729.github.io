---
title: ESM Modules
author: Shailesh Kumar
weight: 1
date: 2025-09-26
---

Remember those early days of programming? You’d have a massive JavaScript file with all your code lumped together, or worse, you’d have multiple files and rely on the browser to load them in the correct order. Things got messy, and managing dependencies felt like a chaotic game of dominoes. Then came module systems like CommonJS, which brought some much-needed order to the chaos, but what if there was a way to do it natively? This tutorial will guide you through **ESM (ECMAScript Modules)**, the modern standard for writing modular JavaScript. We'll explore why it exists, how it works, and how to use it to refactor a legacy backend project into a clean, well-structured application.

## ESM 101: A Quick Refresher

### The Old Way: CommonJS

Before the advent of native modules, `Node.js` created its own system to manage dependencies. This system, called **CommonJS**, solved the "spaghetti code" problem by allowing you to break your application into manageable, reusable files. You'd **export** code from one file using `module.exports` and then **import** it into another using the `require()` function. This system was revolutionary at the time, but it had a key limitation: it was **synchronous**, meaning that modules were loaded sequentially as the code executed.

Let's look at a simple example with a `require` statement to see how it works.

```JavaScript
// utils.js
const add = (a, b) => {
  return a + b;
};

module.exports = {
  add,
};

// app.js
const { add } = require('./utils.js');

const result = add(5, 10);
console.log(result); // Output: 15
```

**Walkthrough:**

1. In `utils.js`, we define a function called `add`.
2. We explicitly tell Node.js to **export** this function using `module.exports`. We're packaging up what we want to share.
3. In `app.js`, we use `require('./utils.js')` to **import** the code we exported from the `utils` file. The path is local, so we use `./`.
4. The `require` function returns the object that we assigned to `module.exports`, and we use object destructuring to pull out the `add` function.
5. We can now use the `add` function in `app.js` as if it were defined locally.

### The New Way: ESM Syntax

**ECMAScript Modules (ESM)** is the official, native module system for JavaScript. It was designed to work not just in Node.js, but also in browsers and other environments. Unlike CommonJS, ESM is **asynchronous** and **static**. This means that module dependencies are determined before the code runs, allowing for better tooling and optimizations, such as **tree-shaking**.

```JavaScript
// utils.js
export const add = (a, b) => {
  return a + b;
};

// app.js
import { add } from './utils.js';

const result = add(5, 10);
console.log(result); // Output: 15
```

**Walkthrough:**

1. In `utils.js`, we simply add the `export` keyword in front of the `add` function. This tells JavaScript to make this function available for others to use.
2. In `app.js`, we use the `import` keyword to grab the `add` function from `utils.js`. Notice the syntax is slightly different—it's more explicit about what you're importing.
3. Just like before, we can now use the `add` function in `app.js`.

**Note:** When importing your own local files, **you must include the full file extension** (e.g., `.js`). This differs from CommonJS, where the extension can often be omitted. This strictness ensures consistency and compatibility across all environments.
## The Key Differences in Depth

While the syntax is the most apparent difference between CommonJS and ESM, the fundamental shift is in their core design philosophies. Understanding these two key distinctions will help you appreciate the full power of native modules.
### Static vs. Dynamic: A Fundamental Shift

The most critical difference is that ESM is **static**. This means that the relationships between your modules—what’s being imported and exported—are determined at **compile-time**, before a single line of your code is executed. Think of it like creating a detailed grocery list before you even leave the house. Your tools can examine all your import statements and create a comprehensive map of your application's dependencies.

This static nature allows for powerful optimizations that were not possible with CommonJS. The most famous example is **tree-shaking**, a process where build tools can automatically detect and eliminate any code that is exported from a module but never actually imported and used by your application. This can significantly reduce the size of your final application, thereby improving its performance.

CommonJS, on the other hand, is a dynamic module system. The `require()` function is a regular function call that happens at **run-time**. The module isn’t loaded until that line is executed. This offers flexibility—you can conditionally `require` a module inside an `if` statement—but it comes at the cost of performance and the ability to perform static analysis.
### Asynchronous Loading & Dynamic Imports

Another significant difference is that ESM is designed for **asynchronous** loading. This means that modules are loaded in a non-blocking way, which is essential for environments like the browser, where you don’t want a single script to freeze the entire page. While CommonJS loads modules **synchronously** (one after another), ESM can fetch and load modules simultaneously, significantly reducing the initial load time of a complex application.

This asynchronous nature is also what enables a powerful ESM feature: **dynamic imports**. This allows you to load a module only when needed, rather than at the beginning of your application. This is a game-changer for performance.

```JavaScript
// A simple example of an asynchronous dynamic import
async function getRecipe(recipeId) {
  const { fetchRecipe } = await import('./data/recipes.js');
  const recipe = await fetchRecipe(recipeId);
  return recipe;
}
```

**Walkthrough:**

1. The `getRecipe` function uses `await import()` to **dynamically** and **asynchronously** load the `recipes.js` module only when the function is called.
2. The `import()` call returns a `Promise`, and `await` pauses the function's execution until the module is loaded.
3. Once the module is available, we can access and use its `fetchRecipe` function.

This approach is perfect for scenarios where you need to load a specific feature only when a user interacts with it, reducing your initial startup time.
## The Node.js Difference: Why "type": "module" Matters

When it comes to the backend, the most significant factor in how your code runs is what Node.js thinks your files are. By default, Node.js treats `.js` files as **CommonJS modules**. To tell Node.js to use the new native module system, you have to flip a switch in your project's configuration.
### The "type" Switch

That switch is a simple key-value pair in your `package.json` file:

```JSON
{
  "name": "medication-reminder-api",
  "version": "1.0.0",
  "description": "A simple API to manage medication reminders.",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  }
}
```

By adding `"type": "module"`, you're telling Node.js to interpret all files with a `.js` extension within this project as **ESM modules**. Without this setting, Node.js will assume your code is CommonJS and throw errors if you use `import` or `export` syntax.
### Farewell, Globals

One of the most significant and often frustrating changes for developers migrating from CommonJS is the loss of familiar global variables. In an ESM file, you no longer have access to `require`, `exports`, `module.exports`, `__filename`, or `__dirname`. This is a core part of the ESM design, which aims for a more explicit and dependency-free environment.

For example, getting the path to the current directory, a common task in backend applications, now requires a different approach:

```JavaScript
// The Old Way (CommonJS)
const path = require('path');

const currentDirPath = __dirname;
console.log(currentDirPath);

// The New Way (ESM)
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
console.log(__dirname);
```

**Walkthrough:**

1. In ESM, the `import.meta.url` object gives you the full URL of the current module file.
2. We use the Node.js built-in `fileURLToPath` utility to convert this URL to a standard file path.
3. Then, we use the `dirname` function from the `path` module to extract the directory name from the file path.

### New Rules: Strict Mode and File Extensions

ESM has a few other built-in behaviors that make for a cleaner codebase:

- **Strict Mode**: All ESM code runs in strict mode by default. This is a good thing! It enforces better coding practices by preventing you from using undeclared variables or other potentially unsafe actions.
- **File Extensions**: If you want to use ESM in a project that is otherwise CommonJS (without the `"type": "module"` setting), you can simply use the `.mjs` file extension for your ESM files. Node.js will automatically treat any file with a `.mjs` extension as an ESM module.

We've covered the what and why of ESM, from its declarative syntax to the robust static and asynchronous design that sets it apart from CommonJS. Now, it’s time to put that knowledge to the test! In the following sections, we will address a common yet challenging real-world problem for many backend developers: migrating an old-school CommonJS project to a modern, efficient ESM codebase. Let's dig in and get our hands dirty.

## The Problem: The Old-School Medication Reminder API

Our starting point is a legacy Node.js backend for a medication reminder system. It's functional, but it's built with old conventions, relying on CommonJS for dependency management. The code is somewhat disorganized, with functions and logic for different API routes all combined into a single file.

Let's imagine our API's main entry point, `index.js`, looks like this:

```JavaScript
// index.js
const express = require('express');

const app = express();
const PORT = 3000;

// A "database" of medications
const medications = [
  { id: 1, name: 'Lisinopril', dose: '10mg', frequency: 'daily' },
  { id: 2, name: 'Metformin', dose: '500mg', frequency: 'twice daily' }
];

// Helper function to find a medication
function findMedicationById(id) {
  return medications.find(med => med.id === id);
}

// GET /api/medications
app.get('/api/medications', (req, res) => {
  res.json(medications);
});

// GET /api/medications/:id
app.get('/api/medications/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const medication = findMedicationById(id);

  if (medication) {
    res.json(medication);
  } else {
    res.status(404).json({ message: 'Medication not found' });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
```

**Walkthrough**

1. The first line uses the **synchronous `require()`** function to import the `express` package. All dependencies are loaded at **run-time**, which, as we discussed, can hinder performance and tooling.
2. All our application logic, including the "database" and helper function, is still contained within this single `index.js` file. This is a common pain point in legacy projects. Although the code is functional, it lacks modularity and is not easily reusable.
3. The API routes are defined using the intuitive `app.get()` syntax. Express handles the heavy lifting, but the underlying module system is still CommonJS.

The project's package.json file defines its identity and dependencies. In a CommonJS project, it's typically simple, with Express listed as a dependency. The absence of `"type": "module"` signals to Node.js that the files should be treated as CommonJS.

```JSON
{
  "name": "medication-reminder-api",
  "version": "1.0.0",
  "description": "An old-school API to manage medication reminders.",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

---

This is a prime example of a legacy codebase that is ripe for modernization. Our goal is to refactor this code into a clean, modular structure using ESM.

## The Solution: ESM and a Modern Structure

Now that we have a clear understanding of the problems in our old CommonJS codebase, let's solve them. The solution involves a two-step process:

1. We'll convert our project to use the **ESM** module system.
2. We'll refactor our single `index.js` file into a clean, **modular** structure with separate files for our data and routes.

By the end of this section, our application will be more readable, reusable, and ready to leverage the full power of modern JavaScript.

### Step 1: Updating `package.json`

The first step is to tell Node.js to treat our project's files as ESM modules. We do this by adding the `"type": "module"` property to our `package.json` file.

```JSON
{
  "name": "medication-reminder-api",
  "version": "1.0.0",
  "description": "A modern, ESM-based API to manage medication reminders.",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

This simple change is the gateway to our new, modular codebase.

### Step 2: Modularizing the Code

Next, we'll break our monolithic `index.js` file into three logical parts: the data, the routes, and the server setup.

#### `medications.js`

This file will be dedicated to managing our medication data. It will export a `medications` array and a function to find a medication by its ID.

```JavaScript
// medications.js
export const medications = [
  { id: 1, name: 'Lisinopril', dose: '10mg', frequency: 'daily' },
  { id: 2, name: 'Metformin', dose: '500mg', frequency: 'twice daily' }
];

export function findMedicationById(id) {
  return medications.find(med => med.id === id);
}
```

**Walkthrough:**

1. We use the **ESM `export` keyword** to expose both the `medications` array and the `findMedicationById` function explicitly. This makes them available for other files to import.

#### `routes.js`

This file will contain all our API routes. We'll use Express's built-in `Router` to create a modular set of endpoints.

```JavaScript
// routes.js
import { Router } from 'express';
import { medications, findMedicationById } from './medications.js';

const router = Router();

// GET /api/medications
router.get('/medications', (req, res) => {
  res.json(medications);
});

// GET /api/medications/{id}
router.get('/medications/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const medication = findMedicationById(id);

  if (medication) {
    res.json(medication);
  } else {
    res.status(404).json({ message: 'Medication not found' });
  }
});

export default router;
```

**Walkthrough:**

1. We use **ESM `import` statements** to load the `Router` from `express` and our data and helper function from the new `medications.js` file.
2. The file extension `.js` is **required** for local imports in ESM.
3. We define our routes using the `router` object.
4. Finally, we use `export default router` to export the entire router, making all our defined routes available to our main application file.

#### `index.js`

Our main entry point is now significantly simplified. It simply sets up the server and registers the routes we created in `routes.js`.

```JavaScript
// index.js
import express from 'express';
import medicationRoutes from './routes.js';

const app = express();
const PORT = 3000;

// Register our routes with the app
app.use('/api', medicationRoutes);

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
```

**Walkthrough:**

1. We use `import` to load the `express` library and our `medicationRoutes` from the `routes.js` file.
2. The `app.use('/api', medicationRoutes)` line tells Express to use all the routes defined in our `routes.js` file and prefix them with `/api`.
3. The rest of the file is dedicated to setting up and starting the server, which is its only concern.

By separating our code into clear, logical modules, we've solved the problem of a monolithic codebase. The application is now easier to read, maintain, and scale. We've also successfully migrated from the synchronous CommonJS system to the powerful, asynchronous ESM.

## Interoperability & The Library Creator's Dilemma

Migrating your own code is one thing, but what happens when the libraries you depend on haven't made the full jump to ESM? Or worse, when they've made the jump in a way that breaks your code? The transition from CommonJS to ESM can be complex, particularly in terms of interoperability.

### The Problem: A Tale of Two Module Systems

As a backend developer, you often use libraries to solve specific problems. But what if one version of a library works only with CommonJS, and the next version is ESM-only? This situation forces you to either stick with an old version or rewrite your code to match the new module system.

This problem is particularly tricky for library creators themselves. They want their code to be usable by both legacy and modern projects. The solution lies in a key feature of the ESM specification: **conditional exports** in `package.json`.

### Conditional Exports: The Solution

Conditional exports allow a library to define different entry points based on the context in which it's being used. This means the library can serve up an ESM version to a project that uses `import` and a CommonJS version to a project that uses `require`, all from the same package.

Here's an example of what a `package.json` might look like for a dual-module library:

```JSON
// package.json for a dual-module library
{
  "name": "my-cool-library",
  "version": "1.0.0",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

**Walkthrough:**

1. The `exports` field tells Node.js how to resolve the main entry point for the package.
2. The `"import"` key points to the ESM version of the code (`./dist/esm/index.js`). A project that uses `import { someFunc } from 'my-cool-library'` will get this file.
3. The `"require"` key points to the CommonJS version (`./dist/cjs/index.js`). A project that uses `const { someFunc } = require('my-cool-library')` will get this file.

This simple configuration solves the dual-module dilemma, ensuring the library is compatible with both systems. Many popular libraries, including `yargs` and `chalk`, have adopted this approach to support their broad user base.

### A Practical Example

To truly understand how a single library can serve both CommonJS and ESM users, let's build a small example. We'll create a simple library called **`math-utils`**, split across two files. In a real-world scenario, you would write your source code and then use a build tool (like Babel, Rollup, or esbuild) to compile it into two different formats: one for CommonJS and one for ESM.

#### Step 1: The Source Code

Let's assume our source code, written in a modern syntax, looks like this. We'll have a main file that re-exports a utility function from another file.

```JavaScript
// src/add.js
export const add = (a, b) => a + b;

// src/index.js
export * from './add.js';
```

#### Step 2: The Compiled Output

Our build tool would take this source code and create two separate output folders:

**CommonJS Output (`dist/cjs`)**

```JavaScript
// dist/cjs/add.js
const add = (a, b) => a + b;
exports.add = add;

// dist/cjs/index.js
const add = require('./add.js');
Object.defineProperty(exports, "__esModule", { value: true });
exports.add = add.add;
```

**ESM Output (`dist/esm`)**

```JavaScript
// dist/esm/add.js
export const add = (a, b) => a + b;

// dist/esm/index.js
export * from './add.js';
```

We now have two different versions of our library, and we need a way for Node.js to determine which one to serve.

#### Step 3: The `package.json` Solution

This is where the `exports` field comes in. We'll configure our `package.json` file to instruct Node.js to use the correct version, depending on whether a consumer uses an `import` or a `require` statement.

```JSON
{
  "name": "math-utils",
  "version": "1.0.0",
  "main": "dist/cjs/index.js",
  "type": "commonjs",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

**Walkthrough:**

1. **`"main"` and `"type"`**: The `main` field is a fallback for older versions of Node.js that don't support the `exports` field, ensuring our library remains backward compatible. We set `"type": "commonjs"` to align with this.
2. **The `"exports"` field**: This is the modern entry point. It contains a period `.` which represents the root of the package.
3. **`"import"` condition**: This condition tells Node.js to use the file `dist/esm/index.js` if the library is being loaded with an `import` statement in an ESM context.
4. **`"require"` condition**: This condition tells Node.js to use the file `dist/cjs/index.js` if the library is being loaded with a `require()` statement in a CommonJS context.

This elegant solution enables a single library to serve both modern and legacy projects without requiring any special action on the user's part. They use their preferred module syntax, and Node.js figures out the rest.
### The Build Process

We showed you the compiled output of our `math-utils` library. But how do we get that output? This is where a **build tool** comes in.

The build process is a critical step that translates your modern, clean source code into different formats that can be run in various environments. Think of it like a coffee machine that takes the same coffee beans but can produce an espresso, a latte, or a cold brew.

The process typically involves three steps:

1. **The Source:** You write your library's source code using modern JavaScript, often with ESM syntax (`import`/`export`) for consistency.
2. **The Build Tool:** You use a tool like **Rollup**, **esbuild**, or **Babel** to process your source files.1 You configure the tool to create two separate output bundles.2
3. **The Output:** The build tool generates two distinct directories, a CommonJS version and an ESM version.3 These are the files that end up in the `dist` folder we saw earlier.

This process ensures that you only have to maintain a single set of source files, while still catering to both CommonJS and ESM consumers.
### Comparing Build Tools

When choosing a build tool, it's helpful to know what each one excels at. While all can handle our dual-module problem, they have different strengths and philosophies.

- **Babel**: More of a **transpiler** than a bundler, Babel's primary purpose is to convert modern JavaScript into older, backward-compatible versions.4 It's incredibly flexible and has a huge ecosystem of plugins and presets.5 If your project needs to support ancient browser versions or requires complex syntax transformations (like JSX for React), Babel is a robust and reliable choice.
- **Rollup**: This tool is specifically designed for building **JavaScript libraries**. It's renowned for its highly efficient **tree-shaking** capabilities, which eliminate unused code to produce tiny and optimized bundles. This makes it perfect for the `math-utils` example we just built, where bundle size is a key concern for library consumers.
- **esbuild**: If **speed** is your top priority, esbuild is a game-changer. Written in Go, it can bundle and transpile code at lightning-fast speeds, often 10 to 100 times faster than other tools. While it's not as configurable as Babel or as focused on libraries as Rollup, its simplicity and raw performance make it an excellent choice for rapid development and building applications.

### Building the `math-utils` Library with `esbuild`

To build the dual-module `math-utils` library, we'll use `esbuild` to compile our modern source code into both a CommonJS and an ESM format. This process will produce the `dist` folder we discussed earlier, ready to be published and used by any project.

#### Step 1: Set Up the Project

First, create the project directory, initialize it, and install `esbuild` as a development dependency.

```Bash
mkdir math-utils
cd math-utils
npm init -y
npm install esbuild --save-dev
```

Next, create a `src` folder with the following two files:

```JavaScript
// src/add.js
export const add = (a, b) => a + b;

// src/index.js
export * from './add.js';
```

---

#### Step 2: The `package.json` File

This is where all our configuration comes together. We'll add the `exports` field to handle dual-module support and create a simple script to automate the build process.

```JSON
{
  "name": "math-utils",
  "version": "1.0.0",
  "main": "dist/cjs/index.js",
  "type": "commonjs",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  },
  "scripts": {
    "build:esm": "esbuild src/index.js --bundle --outdir=dist/esm --format=esm",
    "build:cjs": "esbuild src/index.js --bundle --outdir=dist/cjs --format=cjs",
    "build": "npm run build:cjs && npm run build:esm"
  },
  "devDependencies": {
    "esbuild": "^0.19.5"
  }
}
```

#### Step 3: Run the Build

From your terminal, simply run the build script we just created.

```Bash
npm run build
```

**Walkthrough of the `esbuild` Commands**

- `npm run build`: This runs both of our build scripts one after the other.
- `esbuild src/index.js`: Sets our main entry point for the library.
- `--bundle`: This is a crucial flag that tells `esbuild` to bundle all of our source files into a single output file.
- `--outdir=dist/esm`: This specifies the output directory for our bundled files. The first command creates a folder called `esm` inside of our `dist` folder.
- `--format=esm`: This tells `esbuild` to compile the output using **ESM syntax**.
- `--format=cjs`: This tells `esbuild` to compile the output using **CommonJS syntax**.

After running the command, your project will now have a `dist` folder that looks like this:

```
dist/
├── cjs/
│   └── index.js   (CommonJS output)
└── esm/
    └── index.js   (ESM output)
```

This elegant process allows you to maintain a single source of truth while providing your library's consumers with the correct module system for their project.

You might be a bit surprised why the `package.json` says `"type": "commonjs"` when the source code is written using ESM syntax. A `package.json` file may specify `"type": "commonjs"` even when the source code is written using ESM syntax because the project is designed to be consumed by both modern and legacy JavaScript environments. This is a common practice for library creators who want to ensure their code works for the broadest possible audience.

#### The Dual-Module Strategy

The core reason behind this strategy is a **build process** that transforms the modern ESM source code into a backward-compatible CommonJS version. The `package.json` file then acts as a map, directing different environments to the correct file format.

1. **Source Code:** The developer writes their library code using the clean, modern ESM syntax (`import`/`export`). This is the single source of truth that is easier to maintain and develop.
2. **The Build:** A build tool, such as **Rollup**, **esbuild**, or **Babel**, is used to compile the ESM source code into two separate output folders: one containing the original ESM files and another containing a transpiled CommonJS version.
3. **The `package.json` Map:** The `package.json` file is configured with the `"exports"` field, which tells Node.js which file to use based on the context. The `"type": "commonjs"` field is often included to prevent older versions of Node.js from misinterpreting `.js` files in the package's root.

For example, a `package.json` might include:

```JSON
{
  "name": "my-library",
  "type": "commonjs",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

When a user's code uses an `import` statement, Node.js sees the `"import"` condition in the `exports` field and loads the modern ESM file from `./dist/esm`. Conversely, when a user's code uses a `require()` statement, Node.js sees the `"require"` condition and loads the legacy CommonJS file from `./dist/cjs`.

This strategy is known as creating a **dual-module package**. It ensures that everyone, whether using a modern or legacy project, receives a version of the library that works seamlessly in their environment.
## Interoperability and Testing Tools

Another common pain point is with testing and mocking tools. Tools like `sinon`, which were designed to "spy" on CommonJS modules loaded with `require()`, sometimes don't work as seamlessly with ESM's static `import` syntax.

The reason for this is fundamental: `require()` is a function call that can be intercepted and mocked, but `import` is a **static declaration**. It's more of a directive than a function, and you can't easily intercept it at runtime. This necessitates a shift in design philosophy for testing and mocking dependencies in your application. For some complex mocking scenarios, you may need to use the dynamic `import()` to achieve your goals, as it allows you to load modules at runtime and is more easily mockable.

This is an excellent example of how the move to ESM requires not just a syntax change, but a deeper examination of your application's architecture and tooling.

## The Yargs Library: A Real-World Example

The **`yargs`** library is a popular choice for building powerful command-line tools. However, its transition to being an ESM-first library is a prime example of the challenges developers face when a dependency changes its module system. Let's examine how the approach to using `yargs` differs between a CommonJS project and an ESM project.

### The Old Way: Yargs with CommonJS

In a CommonJS project, using `yargs` is a simple, synchronous process. You install the library, and then `require` it directly into your main file.

**`package.json` (CommonJS)**

```JSON
{
  "name": "yargs-cjs-example",
  "version": "1.0.0",
  "description": "An example using yargs with CommonJS",
  "main": "index.js",
  "scripts": {
    "start": "node index.js --name=World"
  },
  "dependencies": {
    "yargs": "^16.2.0"
  }
}
```

**`index.js` (CommonJS)**

```JavaScript
const yargs = require('yargs');

const argv = yargs
  .option('name', {
    alias: 'n',
    description: 'Your name',
    type: 'string',
  })
  .help()
  .alias('help', 'h')
  .argv;

console.log(`Hello, ${argv.name}!`);
```

**Walkthrough:**

1. We use the **`require()`** function to import the `yargs` library.
2. The `yargs` API is called in a **synchronous, chainable fashion**. The code runs from top to bottom, and the `argv` object is available immediately after the last method call.
3. This approach is simple and effective, but it relies entirely on the CommonJS module system.

### The New Way: Yargs with ESM

Recent versions of `yargs` are ESM-first, meaning they're designed to be consumed with `import` statements. While the core API remains familiar, the module-loading syntax changes, forcing your project to be configured as ESM.

**`package.json` (ESM)**

```JSON
{
  "name": "yargs-esm-example",
  "version": "1.0.0",
  "description": "An example using yargs with ESM",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js --name=World"
  },
  "dependencies": {
    "yargs": "^17.7.2"
  }
}
```

**`index.js` (ESM)**

```JavaScript
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const argv = yargs(hideBin(process.argv))
  .option('name', {
    alias: 'n',
    description: 'Your name',
    type: 'string',
  })
  .help()
  .alias('help', 'h')
  .argv;

console.log(`Hello, ${argv.name}!`);
```

**Walkthrough:**

1. First, we add **`"type": "module"`** to our `package.json` to tell Node.js we are using ESM.
2. We use the **`import`** statement to bring in the `yargs` library. Notice that a helper function, `hideBin`, is now a separate import from the `yargs/helpers` path. This is a common practice in modern ESM libraries, allowing for more efficient tree-shaking.
3. The main `yargs` function is now called with `hideBin(process.argv)` to parse the command-line arguments in an ESM context correctly.

The transition from the CommonJS example to the ESM example is a direct reflection of a library updating its module system. Adapting to these changes is a crucial skill for modern JavaScript developers.
## Summary and Key Learnings

We've journeyed from a fundamental understanding of JavaScript's module systems to the practical application of ESM in a backend environment. The shift from CommonJS to ESM is more than a syntax change; it represents a move toward a more modern, efficient, and standardized approach to building applications.

Here are the key takeaways from our exploration:

- **Syntax Matters:** We saw how the declarative `import` and `export` statements in ESM replace the `require()` function and `module.exports` object.
- **Static and Asynchronous:** ESM's **static** nature enables tools to understand dependencies before a single line of code is executed, allowing for powerful optimizations such as **tree-shaking**. Its **asynchronous** loading prevents blocking, which is a significant performance benefit.
- **The Node.js Switch:** We learned that adding `"type": "module"` to `package.json` is the key to telling Node.js to interpret your files as ESM. This also means giving up CommonJS globals like `__dirname` and `require`.
- **Modularity is Key:** By refactoring our legacy Express API, we saw how a single, monolithic file can be broken down into clear, reusable, and maintainable modules.
- **Advanced Solutions:** We explored the "Library Creator's Dilemma" and learned how the `exports` field in `package.json` allows a single package to support both CommonJS and ESM consumers, a crucial part of the modern ecosystem.

## What's Next? Take Action!

You've gained a solid understanding of ESM and its benefits. The best way to solidify this knowledge is to start applying it. Here are a few challenges to help you take action and continue your learning journey:

1. **Refactor Your Own Project:** Pick a small personal project or a piece of code you’ve written in CommonJS and try to refactor it to use ESM. This will help you get comfortable with the new syntax and common pitfalls.
2. **Explore Dynamic Imports:** Learn more about using `import()` to load modules on the fly. Try to find a scenario in your code where loading a large module only when a specific function is called could improve performance.
3. **Check Out Other Libraries:** Look at some of the popular Node.js libraries you use and explore their documentation to see how they handle ESM and dual-module compatibility. Understanding how others solve this problem will deepen your knowledge.
## References

- **Official Documentation**:
    - [ECMAScript Modules](https://nodejs.org/api/esm.html)
    - [Modules: CommonJS](https://nodejs.org/api/modules.html)
- **Articles and Blogs**:
	- [Using ES modules in Node.js - LogRocket Blog](https://blog.logrocket.com/es-modules-in-node-today/)
	- [CommonJS vs. ES modules in Node.js - LogRocket Blog](https://blog.logrocket.com/commonjs-vs-es-modules-node-js/)
	- [The JavaScript Modules Handbook – Complete Guide to ES Modules and Module Bundlers](https://www.freecodecamp.org/news/javascript-es-modules-and-module-bundlers/)
- **Books**:
	- [Node.js Design Patterns: Master production-grade Node.js applications](https://nodejsdesignpatterns.com/)
    - [Secrets of the JavaScript Ninja, Second Edition - John Resig, Bear Bibeault, and Josip Maras](https://www.manning.com/books/secrets-of-the-javascript-ninja-second-edition)


import filecmp
  expected_status = svntest.actions.get_virginal_state('', 1)
  svntest.actions.run_and_verify_patch('', os.path.abspath(patch_file_path),
  expected_status = svntest.actions.get_virginal_state('', 1)
  svntest.actions.run_and_verify_patch('', os.path.abspath(patch_file_path),
    'D         %s\n' % sbox.ospath('A/B/E'),
  expected_status = svntest.actions.get_virginal_state('', 1)
  svntest.actions.run_and_verify_patch('', os.path.abspath(patch_file_path),
    'Skipped missing target: \'%s\'\n' % skipped_path,
  expected_status = svntest.actions.get_virginal_state('', 1)
  svntest.actions.run_and_verify_patch('', os.path.abspath(patch_file_path),
      'src'                             : Item(status='A ', wc_rev=0),
      'src/tools/ConsoleRunner'         : Item(status='A ', wc_rev=0),
    "--- link\t(revision 1)",
    "+++ link\t(working copy)",
    "+link bardame",
  # r2 - Try as plain text with how we encode the symlink
  svntest.main.file_write(sbox.ospath('link'), 'link foo')
  sbox.simple_add('link')

  expected_output = svntest.wc.State(wc_dir, {
    'link'       : Item(verb='Adding'),
  })
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        None, None, wc_dir)

  patch_output = [
    'U         %s\n' % sbox.ospath('link'),
  svntest.actions.run_and_verify_svn(None, patch_output, [],
                                     'patch', patch_file_path, wc_dir)

  # r3 - Store result
  expected_output = svntest.wc.State(wc_dir, {
    'link'       : Item(verb='Sending'),
  })
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        None, None, wc_dir)

  # r4 - Now as symlink
  sbox.simple_rm('link')
  sbox.simple_add_symlink('foo', 'link')
  expected_output = svntest.wc.State(wc_dir, {
    'link'       : Item(verb='Replacing'),
  })
  svntest.actions.run_and_verify_commit(wc_dir, expected_output,
                                        None, None, wc_dir)

  svntest.actions.run_and_verify_svn(None, patch_output, [],
                                     'patch', patch_file_path, wc_dir)


  # BH: easy check for node type: a non symlink would show as obstructed
  expected_status = svntest.actions.get_virginal_state(wc_dir, 1)
  expected_status.add({
    'link'              : Item(status='M ', wc_rev='4'),
  })
  svntest.actions.run_and_verify_status(wc_dir, expected_status)

def patch_replace_dir_with_file_and_vv(sbox):
  "replace dir with file and file with dir"
  sbox.build(read_only=True)

  patch_file_path = make_patch_path(sbox)
  svntest.main.file_write(patch_file_path, ''.join([
  # Delete all files in D and descendants to delete D itself
    "Index: A/D/G/pi\n",
    "===================================================================\n",
    "--- A/D/G/pi\t(revision 1)\n",
    "+++ A/D/G/pi\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'pi'.\n",
    "Index: A/D/G/rho\n",
    "===================================================================\n",
    "--- A/D/G/rho\t(revision 1)\n",
    "+++ A/D/G/rho\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'rho'.\n",
    "Index: A/D/G/tau\n",
    "===================================================================\n",
    "--- A/D/G/tau\t(revision 1)\n",
    "+++ A/D/G/tau\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'tau'.\n",
    "Index: A/D/H/chi\n",
    "===================================================================\n",
    "--- A/D/H/chi\t(revision 1)\n",
    "+++ A/D/H/chi\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'chi'.\n",
    "Index: A/D/H/omega\n",
    "===================================================================\n",
    "--- A/D/H/omega\t(revision 1)\n",
    "+++ A/D/H/omega\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'omega'.\n",
    "Index: A/D/H/psi\n",
    "===================================================================\n",
    "--- A/D/H/psi\t(revision 1)\n",
    "+++ A/D/H/psi\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'psi'.\n",
    "Index: A/D/gamma\n",
    "===================================================================\n",
    "--- A/D/gamma\t(revision 1)\n",
    "+++ A/D/gamma\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'gamma'.\n",
  # Delete iota
    "Index: iota\n",
    "===================================================================\n",
    "--- iota\t(revision 1)\n",
    "+++ iota\t(working copy)\n",
    "@@ -1 +0,0 @@\n",
    "-This is the file 'iota'.\n",

  # Add A/D as file
    "Index: A/D\n",
    "===================================================================\n",
    "--- A/D\t(revision 0)\n",
    "+++ A/D\t(working copy)\n",
    "@@ -0,0 +1 @@\n",
    "+New file\n",
    "\ No newline at end of file\n",

  # Add iota as directory
    "Index: iota\n",
    "===================================================================\n",
    "--- iota\t(revision 1)\n",
    "+++ iota\t(working copy)\n",
    "\n",
    "Property changes on: iota\n",
    "___________________________________________________________________\n",
    "Added: k\n",
    "## -0,0 +1 ##\n",
    "+v\n",
    "\ No newline at end of property\n",
  ]))

  expected_output = [
    'D         %s\n' % sbox.ospath('A/D/G/pi'),
    'D         %s\n' % sbox.ospath('A/D/G/rho'),
    'D         %s\n' % sbox.ospath('A/D/G/tau'),
    'D         %s\n' % sbox.ospath('A/D/G'),
    'D         %s\n' % sbox.ospath('A/D/H/chi'),
    'D         %s\n' % sbox.ospath('A/D/H/omega'),
    'D         %s\n' % sbox.ospath('A/D/H/psi'),
    'D         %s\n' % sbox.ospath('A/D/H'),
    'D         %s\n' % sbox.ospath('A/D/gamma'),
    'D         %s\n' % sbox.ospath('A/D'),
    'D         %s\n' % sbox.ospath('iota'),
    'A         %s\n' % sbox.ospath('A/D'),
    'A         %s\n' % sbox.ospath('iota'),
  ]

  svntest.actions.run_and_verify_svn(None, expected_output, [],
                                     'patch', patch_file_path, sbox.wc_dir)

@Issue(4297)
def single_line_mismatch(sbox):
  "single line replacement mismatch"

  sbox.build()
  wc_dir = sbox.wc_dir
  patch_file_path = make_patch_path(sbox)
  svntest.main.file_write(patch_file_path, ''.join([
    "Index: test\n",
    "===================================================================\n",
    "--- test\t(revision 1)\n",
    "+++ test\t(working copy)\n",
    "@@ -1 +1 @@\n",
    "-foo\n",
    "\\ No newline at end of file\n",
    "+bar\n",
    "\\ No newline at end of file\n"
    ]))

  # r2 - Try as plain text with how we encode the symlink
  svntest.main.file_write(sbox.ospath('test'), 'line')
  sbox.simple_add('test')
  sbox.simple_commit()

  # And now this patch should fail, as 'line' doesn't equal 'foo'
  # But yet it shows up as deleted instead of conflicted
  expected_output = [
    'C         %s\n' % sbox.ospath('test'),
    '>         rejected hunk @@ -1,1 +1,1 @@\n',
    'Summary of conflicts:\n',
    '  Text conflicts: 1\n',
  ]

  svntest.actions.run_and_verify_svn(None, expected_output, [],
@Issue(3644)
def patch_empty_file(sbox):
  "apply a patch to an empty file"

  sbox.build()
  wc_dir = sbox.wc_dir

  patch_file_path = make_patch_path(sbox)
  svntest.main.file_write(patch_file_path, ''.join([
  # patch a file containing just '\n' to 'replacement\n'
    "Index: lf.txt\n",
    "===================================================================\n",
    "--- lf.txt\t(revision 2)\n",
    "+++ lf.txt\t(working copy)\n",
    "@@ -1 +1 @@\n",
    "\n"
    "+replacement\n",

  # patch a new file 'new.txt\n'
    "Index: new.txt\n",
    "===================================================================\n",
    "--- new.txt\t(revision 0)\n",
    "+++ new.txt\t(working copy)\n",
    "@@ -0,0 +1 @@\n",
    "+new file\n",

  # patch a file containing 0 bytes to 'replacement\n'
    "Index: empty.txt\n",
    "===================================================================\n",
    "--- empty.txt\t(revision 2)\n",
    "+++ empty.txt\t(working copy)\n",
    "@@ -0,0 +1 @@\n",
    "+replacement\n",
  ]))

  sbox.simple_add_text('', 'empty.txt')
  sbox.simple_add_text('\n', 'lf.txt')
  sbox.simple_commit()

  expected_output = [
    'U         %s\n' % sbox.ospath('lf.txt'),
    'A         %s\n' % sbox.ospath('new.txt'),
    'U         %s\n' % sbox.ospath('empty.txt'),
    # Not sure if this line is necessary, but it doesn't hurt
    '>         applied hunk @@ -0,0 +1,1 @@ with offset 0\n',
  ]

  # Current result: lf.txt patched ok, new created, empty succeeds with offset.
  svntest.actions.run_and_verify_svn(None, expected_output, [],
                                     'patch', patch_file_path, wc_dir)

  expected_disk = svntest.main.greek_state.copy()
  expected_disk.add({
    'lf.txt'            : Item(contents="\n"),
    'new.txt'           : Item(contents="new file\n"),
    'empty.txt'         : Item(contents="replacement\n"),
  })

  svntest.actions.verify_disk(wc_dir, expected_disk)

@Issue(3362)
def patch_apply_no_fuz(sbox):
  "svn diff created patch should apply without fuz"

  sbox.build(read_only=True)
  wc_dir = sbox.wc_dir

  svntest.main.file_write(sbox.ospath('test.txt'), '\n'.join([
      "line_1",
      "line_2",
      "line_3",
      "line_4",
      "line_5",
      "line_6",
      "line_7",
      "line_8",
      "line_9",
      "line_10",
      "line_11",
      "line_12",
      "line_13",
      "line_14",
      "line_15",
      "line_16",
      "line_17",
      "line_18",
      "line_19",
      "line_20",
      "line_21",
      "line_22",
      "line_23",
      "line_24",
      "line_25",
      "line_26",
      "line_27",
      "line_28",
      "line_29",
      "line_30",
      ""
    ]))
  svntest.main.file_write(sbox.ospath('test_v2.txt'), '\n'.join([
      "line_1a",
      "line_1b",
      "line_1c",
      "line_1",
      "line_2",
      "line_3",
      "line_4",
      "line_5a",
      "line_5b",
      "line_5c",
      "line_6",
      "line_7",
      "line_8",
      "line_9",
      "line_10",
      "line_11a",
      "line_11b",
      "line_11c",
      "line_12",
      "line_13",
      "line_14",
      "line_15",
      "line_16",
      "line_17",
      "line_18",
      "line_19a",
      "line_19b",
      "line_19c",
      "line_20",
      "line_21",
      "line_22",
      "line_23",
      "line_24",
      "line_25",
      "line_26",
      "line_27a",
      "line_27b",
      "line_27c",
      "line_28",
      "line_29",
      "line_30",
      ""
    ]))

  sbox.simple_add('test.txt', 'test_v2.txt')

  result, out_text, err_text = svntest.main.run_svn(None,
                                                    'diff',
                                                    '--old',
                                                    sbox.ospath('test.txt'),
                                                    '--new',
                                                    sbox.ospath('test_v2.txt'))

  patch_path = sbox.ospath('patch.diff')
  svntest.main.file_write(patch_path, ''.join(out_text))

  expected_output = [
    'G         %s\n' % sbox.ospath('test.txt'),
  ]

  # Current result: lf.txt patched ok, new created, empty succeeds with offset.
  svntest.actions.run_and_verify_svn(None, expected_output, [],
                                     'patch', patch_path, wc_dir)

  if not filecmp.cmp(sbox.ospath('test.txt'), sbox.ospath('test_v2.txt')):
    raise svntest.Failure("Patch result not identical")


              patch_replace_dir_with_file_and_vv,
              single_line_mismatch,
              patch_empty_file,
              patch_apply_no_fuz,
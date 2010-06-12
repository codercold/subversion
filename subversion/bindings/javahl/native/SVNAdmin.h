/**
 * @copyright
 * ====================================================================
 *    Licensed to the Apache Software Foundation (ASF) under one
 *    or more contributor license agreements.  See the NOTICE file
 *    distributed with this work for additional information
 *    regarding copyright ownership.  The ASF licenses this file
 *    to you under the Apache License, Version 2.0 (the
 *    "License"); you may not use this file except in compliance
 *    with the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing,
 *    software distributed under the License is distributed on an
 *    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *    KIND, either express or implied.  See the License for the
 *    specific language governing permissions and limitations
 *    under the License.
 * ====================================================================
 * @endcopyright
 *
 * @file SVNAdmin.h
 * @brief Interface of the class SVNAdmin
 */

#ifndef SVNADMIN_H
#define SVNADMIN_H

#include <jni.h>
#include "svn_repos.h"
#include "SVNBase.h"
#include "Revision.h"
#include "OutputStream.h"
#include "InputStream.h"
#include "MessageReceiver.h"
#include "ReposNotifyCallback.h"
#include "StringArray.h"
#include "File.h"

class SVNAdmin : public SVNBase
{
 public:
  void rmlocks(File &path, StringArray &locks);
  jobject lslocks(File &path);
  void verify(File &path, Revision &revisionStart, Revision &revisionEnd,
              ReposNotifyCallback *notifyCallback);
  void setRevProp(File &path, Revision &revision,
                  const char *propName, const char *propValue,
                  bool usePreRevPropChangeHook,
                  bool usePostRevPropChangeHook);
  void rmtxns(File &path, StringArray &transactions);
  jlong recover(File &path);
  void lstxns(File &path, MessageReceiver &messageReceiver);
  void load(File &path, InputStream &dataIn, OutputStream &messageOut,
            bool ignoreUUID, bool forceUUID, bool usePreCommitHook,
            bool usePostCommitHook, const char *relativePath);
  void listUnusedDBLogs(File &path,
                        MessageReceiver &messageReceiver);
  void listDBLogs(File &path, MessageReceiver &messageReceiver);
  void hotcopy(File &path, File &targetPath, bool cleanLogs);
  void dump(File &path, OutputStream &dataOut, OutputStream &messageOut,
            Revision &revsionStart, Revision &RevisionEnd,
            bool incremental, bool useDeltas);
  void deltify(File &path, Revision &start, Revision &end);
  void create(File &path, bool ignoreUUID, bool forceUUID, File &configPath,
              const char *fstype);
  SVNAdmin();
  virtual ~SVNAdmin();
  void dispose(jobject jthis);
  static SVNAdmin *getCppObject(jobject jthis);

 private:
  static svn_error_t *getRevnum(svn_revnum_t *revnum,
                                const svn_opt_revision_t *revision,
                                svn_revnum_t youngest, svn_repos_t *repos,
                                apr_pool_t *pool);
};

#endif // SVNADMIN_H
